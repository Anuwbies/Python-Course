from datetime import datetime, timedelta, timezone
from pathlib import Path
import secrets
import jwt
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from project import create_app
from storage import Job, Report, process_one

class IsolatedCache:
    """Test adapter only: these tests do not establish Redis TTL/network behavior."""
    def __init__(self):
        self.data = {}
    def ping(self):
        return True
    def get(self, key):
        return self.data.get(key)
    def set(self, key, value, ex):
        assert ex == 30
        self.data[key] = value
    def close(self):
        self.data.clear()

def prepare(tmp_path):
    url = "sqlite+pysqlite:///" + (tmp_path / "operations.sqlite").as_posix()
    config = Config(str(Path(__file__).with_name("alembic.ini")))
    config.set_main_option("sqlalchemy.url",url)
    command.upgrade(config,"head")
    engine = create_engine(url,connect_args={"check_same_thread":False})
    key = secrets.token_urlsafe(32)
    return engine, key, create_app(engine, IsolatedCache(), key)

def authorization(key, role):
    now = datetime.now(timezone.utc)
    token = jwt.encode({"sub":"test-user","role":role,"iat":now,"exp":now+timedelta(minutes=5),"aud":"course-api","iss":"course-issuer"},key,algorithm="HS256")
    return {"Authorization":"Bearer "+token}

def test_roles_and_readiness(tmp_path):
    engine,key,app=prepare(tmp_path)
    with TestClient(app) as client:
        assert client.get("/ready").status_code == 200
        assert client.post("/orders",json={"item":"Pen","quantity":2}).status_code == 401
        assert client.post("/orders",headers=authorization(key,"reader"),json={"item":"Pen","quantity":2}).status_code == 403
        response=client.post("/orders",headers=authorization(key,"admin"),json={"item":"Pen","quantity":2})
        assert response.status_code == 201
        assert client.get(f"/orders/{response.json()['id']}",headers=authorization(key,"reader")).status_code == 200
        assert client.get("/metrics",headers=authorization(key,"reader")).status_code == 403

def test_idempotent_job_and_rollback(tmp_path):
    engine,key,app=prepare(tmp_path)
    with TestClient(app) as client:
        headers={**authorization(key,"admin"),"Idempotency-Key":"request-1"}
        client.post("/orders",headers=headers,json={"item":"Pen","quantity":2})
        first=client.post("/reports",headers=headers)
        second=client.post("/reports",headers=headers)
        assert first.status_code == 202
        assert first.json()["id"] == second.json()["id"]
        assert process_one(engine,fail=True)
        with Session(engine) as session:
            assert session.scalar(select(func.count(Report.job_id))) == 0
            job=session.get(Job,first.json()["id"])
            assert job.attempts == 1 and job.status == "pending"
        assert process_one(engine)
        assert not process_one(engine)
        response=client.get(f"/reports/{first.json()['id']}",headers=authorization(key,"reader"))
        assert response.json()["report"] == {"orders":1,"quantity":2}
        assert client.get(f"/reports/{first.json()['id']}",headers=authorization(key,"reader")).json() == response.json()

def test_attempt_limit(tmp_path):
    engine,key,app=prepare(tmp_path)
    with TestClient(app) as client:
        response=client.post("/reports",headers={**authorization(key,"admin"),"Idempotency-Key":"failure"})
        for _ in range(3):
            assert process_one(engine,fail=True)
        assert not process_one(engine)
        with Session(engine) as session:
            job=session.get(Job,response.json()["id"])
            assert job.status == "failed" and job.attempts == 3


def test_invalid_token_contracts(tmp_path):
    engine,key,app=prepare(tmp_path)
    now=datetime.now(timezone.utc)
    valid={"sub":"user","role":"reader","iat":now,"exp":now+timedelta(minutes=5),"aud":"course-api","iss":"course-issuer"}
    tokens=["not-a-token"]
    for changes in [{"exp":now-timedelta(seconds=1)},{"aud":"another-api"},{"iss":"another-issuer"},{"sub":" "},{"role":["admin"]}]:
        tokens.append(jwt.encode({**valid,**changes},key,algorithm="HS256"))
    missing=valid.copy();del missing["role"]
    tokens.append(jwt.encode(missing,key,algorithm="HS256"))
    tokens.append(jwt.encode(valid,secrets.token_urlsafe(32),algorithm="HS256"))
    with TestClient(app) as client:
        for token in tokens:
            response=client.get("/orders/1",headers={"Authorization":"Bearer "+token})
            assert response.status_code == 401
            assert response.headers["www-authenticate"] == "Bearer"
