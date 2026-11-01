from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    item: Mapped[str]
    quantity: Mapped[int]

class OrderInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    item: str = Field(min_length=1)
    quantity: int = Field(gt=0, strict=True)

def create_app(path: Path):
    engine = create_engine(f"sqlite+pysqlite:///{path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    app = FastAPI()
    app.state.engine = engine
    def session_dependency():
        with Session(engine) as session:
            yield session
    @app.post("/orders", status_code=201)
    def create_order(payload: OrderInput, session: Session = Depends(session_dependency)):
        order = Order(**payload.model_dump())
        session.add(order)
        session.commit()
        session.refresh(order)
        return {"id": order.id, "item": order.item, "quantity": order.quantity}
    @app.get("/orders/{identifier}")
    def get_order(identifier: int, session: Session = Depends(session_dependency)):
        order = session.get(Order, identifier)
        if order is None:
            raise HTTPException(404, "Order not found")
        return {"id": order.id, "item": order.item, "quantity": order.quantity}
    return app

def test_restart_persistence(tmp_path):
    path = tmp_path / "orders.sqlite"
    first = create_app(path)
    try:
        with TestClient(first) as client:
            response = client.post("/orders", json={"item": "Pen", "quantity": 2})
            assert response.status_code == 201
            identifier = response.json()["id"]
    finally:
        first.state.engine.dispose()
    second = create_app(path)
    try:
        with TestClient(second) as client:
            response = client.get(f"/orders/{identifier}")
            assert response.status_code == 200
            assert response.json()["item"] == "Pen"
    finally:
        second.state.engine.dispose()

def test_validation(tmp_path):
    app = create_app(tmp_path / "validation.sqlite")
    try:
        with TestClient(app) as client:
            assert client.post("/orders", json={"item": "Pen", "quantity": 0}).status_code == 422
            assert client.get("/orders/1").status_code == 404
    finally:
        app.state.engine.dispose()

def test_missing_order(tmp_path):
    app = create_app(tmp_path / "missing.sqlite")
    try:
        with TestClient(app) as client:
            assert client.get("/orders/999").status_code == 404
    finally:
        app.state.engine.dispose()
