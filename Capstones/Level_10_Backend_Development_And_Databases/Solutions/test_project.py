from pathlib import Path
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text
from project import BASE_DIR, create_app, migrate

def test_http_and_restart(tmp_path):
    url = "sqlite+pysqlite:///" + (tmp_path / "orders.sqlite").as_posix()
    migrate(url)
    first = create_app(url)
    try:
        with TestClient(first) as client:
            assert client.get("/health").status_code == 200
            response = client.post("/orders", json={"item":"Pen","quantity":2})
            assert response.status_code == 201
            identifier = response.json()["id"]
            assert client.post("/orders", json={"item":" ","quantity":2}).status_code == 422
            assert client.post("/orders", json={"item":"Pen","quantity":True}).status_code == 422
            assert client.get("/orders/999").status_code == 404
    finally:
        first.state.engine.dispose()
    second = create_app(url)
    try:
        with TestClient(second) as client:
            assert client.get(f"/orders/{identifier}").json()["item"] == "Pen"
    finally:
        second.state.engine.dispose()

def test_upgrade_preserves_existing_row(tmp_path):
    url = "sqlite+pysqlite:///" + (tmp_path / "migration.sqlite").as_posix()
    config = Config(str(BASE_DIR / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", url)
    command.upgrade(config, "0001")
    engine = create_engine(url)
    try:
        with engine.begin() as connection:
            connection.execute(text("INSERT INTO orders(id,item,quantity) VALUES (1,'Pen',2)"))
        command.upgrade(config, "head")
        with engine.connect() as connection:
            assert connection.execute(text("SELECT note FROM orders WHERE id=1")).scalar_one() == ""
        command.downgrade(config, "0001")
        with engine.connect() as connection:
            assert "note" not in [field["name"] for field in inspect(connection).get_columns("orders")]
            assert connection.execute(text("SELECT quantity FROM orders WHERE id=1")).scalar_one() == 2
    finally:
        engine.dispose()
