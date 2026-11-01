from datetime import datetime
import json
from uuid import uuid4
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (CheckConstraint("quantity BETWEEN 1 AND 100", name="ck_orders_quantity"),
        CheckConstraint("length(trim(item)) BETWEEN 1 AND 80", name="ck_orders_item"),
        CheckConstraint("length(note) <= 120", name="ck_orders_note"))
    id: Mapped[int] = mapped_column(primary_key=True)
    item: Mapped[str] = mapped_column(String(80))
    quantity: Mapped[int]
    note: Mapped[str] = mapped_column(String(120), default="")

class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = (CheckConstraint("attempts BETWEEN 0 AND 3", name="ck_jobs_attempts"),
                     CheckConstraint("status IN ('pending','done','failed')", name="ck_jobs_status"))
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    request_key: Mapped[str] = mapped_column(String(80), unique=True)
    status: Mapped[str] = mapped_column(String(10), default="pending")
    attempts: Mapped[int] = mapped_column(default=0)
    last_error: Mapped[str | None] = mapped_column(String(80), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Report(Base):
    __tablename__ = "reports"
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"), primary_key=True)
    body: Mapped[str] = mapped_column(Text)

def process_one(engine, fail=False):
    """Process one short DB-local report transaction; PostgreSQL coordinates workers."""
    with Session(engine) as session:
        with session.begin():
            statement = select(Job).where(Job.status == "pending", Job.attempts < 3).order_by(Job.created_at, Job.id).with_for_update(skip_locked=True).limit(1)
            job = session.scalar(statement)
            if job is None:
                return False
            job.attempts += 1
            attempt = job.attempts
            session.flush()
            try:
                with session.begin_nested():
                    count, quantity = session.execute(select(func.count(Order.id), func.coalesce(func.sum(Order.quantity), 0))).one()
                    session.add(Report(job_id=job.id, body=json.dumps({"orders": count, "quantity": quantity})))
                    session.flush()
                    if fail:
                        raise RuntimeError("Simulated report failure")
                    job.status = "done"
                    job.last_error = None
                    session.flush()
            except RuntimeError:
                job.status = "failed" if attempt >= 3 else "pending"
                job.last_error = "processing_failure"
    return True
