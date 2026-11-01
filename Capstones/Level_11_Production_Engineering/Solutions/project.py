from contextlib import asynccontextmanager
import json
import logging
from string import ascii_letters, digits
from time import perf_counter
from uuid import uuid4
import jwt
from redis.exceptions import RedisError
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from storage import Job, Order, Report

logger = logging.getLogger(__name__)

class OrderInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    item: str = Field(min_length=1, max_length=80)
    quantity: int = Field(ge=1, le=100, strict=True)
    note: str = Field(default="", max_length=120)

def create_app(engine, cache, key):
    if not isinstance(key, str) or len(key) < 32:
        raise ValueError("TOKEN_SECRET must be configured")
    @asynccontextmanager
    async def lifespan(application):
        try:
            yield
        finally:
            cache.close()
            engine.dispose()
    app = FastAPI(title="Operational shared catalog", lifespan=lifespan)
    metrics = {"requests": 0, "server_errors": 0}
    bearer = HTTPBearer(auto_error=False)
    def session_dependency():
        with Session(engine) as session:
            yield session
    def principal(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
        if credentials is None:
            raise HTTPException(401, "Bearer token required", headers={"WWW-Authenticate":"Bearer"})
        try:
            claims = jwt.decode(credentials.credentials, key, algorithms=["HS256"], audience="course-api", issuer="course-issuer",
                options={"require":["sub","role","iat","exp","aud","iss"]})
            if not isinstance(claims["sub"], str) or not claims["sub"].strip():
                raise jwt.InvalidTokenError("Invalid subject")
            if not isinstance(claims["role"], str) or claims["role"] not in {"reader","admin"}:
                raise jwt.InvalidTokenError("Invalid role")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token", headers={"WWW-Authenticate":"Bearer"})
        return claims
    def admin(claims=Depends(principal)):
        if claims["role"] != "admin":
            raise HTTPException(403, "Admin role required")
        return claims
    @app.middleware("http")
    async def observations(request: Request, call_next):
        supplied = request.headers.get("X-Request-ID", "")
        allowed = set(ascii_letters + digits + "-_.")
        request_id = supplied if supplied and len(supplied) <= 64 and set(supplied) <= allowed else uuid4().hex
        start = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            metrics["requests"] += 1
            metrics["server_errors"] += 1
            route = request.scope.get("route")
            route_name = getattr(route, "path", "unmatched")
            logger.exception("request_id=%s method=%s route=%s status=500 duration_ms=%.3f", request_id, request.method, route_name, (perf_counter()-start)*1000)
            raise
        metrics["requests"] += 1
        metrics["server_errors"] += int(response.status_code >= 500)
        response.headers["X-Request-ID"] = request_id
        route = request.scope.get("route")
        route_name = getattr(route, "path", "unmatched")
        logger.info("request_id=%s method=%s route=%s status=%s duration_ms=%.3f", request_id, request.method, route_name, response.status_code, (perf_counter()-start)*1000)
        return response
    @app.get("/live")
    def live():
        return {"status":"live"}
    @app.get("/ready")
    def ready(session: Session = Depends(session_dependency)):
        try:
            revision = session.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
            cache_ready = cache.ping()
        except (SQLAlchemyError, OSError, RedisError):
            raise HTTPException(503, "Dependencies unavailable")
        if revision != "0003" or not cache_ready:
            raise HTTPException(503, "Dependencies unavailable")
        return {"status":"ready"}
    @app.post("/orders", status_code=201)
    def add_order(payload: OrderInput, claims=Depends(admin), session: Session = Depends(session_dependency)):
        order = Order(**payload.model_dump())
        session.add(order)
        session.commit()
        session.refresh(order)
        return {"id":order.id,"item":order.item,"quantity":order.quantity,"note":order.note}
    @app.get("/orders/{identifier}")
    def get_order(identifier: int, claims=Depends(principal), session: Session = Depends(session_dependency)):
        order = session.get(Order, identifier)
        if order is None:
            raise HTTPException(404, "Order not found")
        return {"id":order.id,"item":order.item,"quantity":order.quantity,"note":order.note}
    @app.post("/reports", status_code=202)
    def enqueue_report(request_key: str = Header(alias="Idempotency-Key", min_length=1, max_length=80), claims=Depends(admin), session: Session = Depends(session_dependency)):
        request_key = request_key.strip()
        if not request_key:
            raise HTTPException(400, "Idempotency key required")
        existing = session.scalar(select(Job).where(Job.request_key == request_key))
        if existing is not None:
            return {"id":existing.id,"status":existing.status}
        job = Job(request_key=request_key)
        session.add(job)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            existing = session.scalar(select(Job).where(Job.request_key == request_key))
            if existing is None:
                raise
            return {"id":existing.id,"status":existing.status}
        session.refresh(job)
        return {"id":job.id,"status":job.status}
    @app.get("/reports/{identifier}")
    def get_report(identifier: str, claims=Depends(principal), session: Session = Depends(session_dependency)):
        job = session.get(Job, identifier)
        if job is None:
            raise HTTPException(404, "Report job not found")
        if job.status != "done":
            return {"id":job.id,"status":job.status,"attempts":job.attempts}
        cache_key = "course:report:" + identifier
        import redis
        try:
            cached = cache.get(cache_key)
        except redis.exceptions.RedisError:
            cached = None
        if cached is not None:
            return {"id":identifier,"status":"done","report":json.loads(cached)}
        report = session.get(Report, identifier)
        try:
            cache.set(cache_key, report.body, ex=30)
        except redis.exceptions.RedisError:
            logger.warning("Report cache unavailable")
        return {"id":identifier,"status":"done","report":json.loads(report.body)}
    @app.get("/metrics")
    def process_metrics(claims=Depends(admin)):
        return dict(metrics)
    return app
