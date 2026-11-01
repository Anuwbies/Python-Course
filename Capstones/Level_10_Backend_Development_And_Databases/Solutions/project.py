import os
from pathlib import Path
from tempfile import TemporaryDirectory

from alembic import command
from alembic.config import Config
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import CheckConstraint, String, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

BASE_DIR = Path(__file__).resolve().parent

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("quantity BETWEEN 1 AND 100", name="ck_orders_quantity"),
        CheckConstraint("length(trim(item)) BETWEEN 1 AND 80", name="ck_orders_item"),
        CheckConstraint("length(note) <= 120", name="ck_orders_note"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    item: Mapped[str] = mapped_column(String(80))
    quantity: Mapped[int]
    note: Mapped[str] = mapped_column(String(120), default="")

class OrderInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    item: str = Field(min_length=1, max_length=80)
    quantity: int = Field(ge=1, le=100, strict=True)
    note: str = Field(default="", max_length=120)

class OrderOutput(OrderInput):
    id: int

def default_url():
    return os.environ.get("DATABASE_URL", "sqlite+pysqlite:///" + (BASE_DIR / "orders.sqlite").as_posix())

def migrate(url):
    config = Config(str(BASE_DIR / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", url)
    command.upgrade(config, "head")

def create_app(url=None):
    url = default_url() if url is None else url
    options = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, connect_args=options)
    application = FastAPI(title="Persistent Order API")
    application.state.engine = engine
    def session_dependency():
        with Session(engine) as session:
            yield session
    def represent(order):
        return {"id": order.id, "item": order.item, "quantity": order.quantity, "note": order.note}
    @application.get("/health")
    def health(session: Session = Depends(session_dependency)):
        try:
            revision = session.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
        except SQLAlchemyError:
            raise HTTPException(503, "Database not ready")
        if revision != "0002":
            raise HTTPException(503, "Database migration required")
        return {"status": "ok"}
    @application.post("/orders", status_code=201, response_model=OrderOutput)
    def create_order(payload: OrderInput, session: Session = Depends(session_dependency)):
        order = Order(**payload.model_dump())
        session.add(order)
        session.commit()
        session.refresh(order)
        return represent(order)
    @application.get("/orders/{identifier}", response_model=OrderOutput)
    def get_order(identifier: int, session: Session = Depends(session_dependency)):
        order = session.get(Order, identifier)
        if order is None:
            raise HTTPException(404, "Order not found")
        return represent(order)
    return application

app = create_app()

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        url = "sqlite+pysqlite:///" + (Path(folder) / "orders.sqlite").as_posix()
        migrate(url)
        first = create_app(url)
        try:
            with TestClient(first) as client:
                created = client.post("/orders", json={"item": "Pen", "quantity": 2})
                identifier = created.json()["id"]
                print(f"Created: {created.status_code}")
                print(f"Invalid: {client.post('/orders', json={'item':'Pen','quantity':0}).status_code}")
                print(f"Missing: {client.get('/orders/999').status_code}")
        finally:
            first.state.engine.dispose()
        second = create_app(url)
        try:
            with TestClient(second) as client:
                print(f"Persisted item: {client.get(f'/orders/{identifier}').json()['item']}")
            with second.state.engine.connect() as connection:
                print(f"Revision: {connection.execute(text('SELECT version_num FROM alembic_version')).scalar_one()}")
        finally:
            second.state.engine.dispose()
