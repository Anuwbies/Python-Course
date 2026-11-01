from sqlalchemy import CheckConstraint, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = (CheckConstraint("amount >= 0"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    amount: Mapped[int]

engine = create_engine("sqlite+pysqlite:///:memory:")
try:
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        with session.begin():
            session.add_all([Expense(category="food", amount=120), Expense(category="food", amount=80), Expense(category="travel", amount=30)])
        statement = select(Expense.category, func.sum(Expense.amount)).group_by(Expense.category).order_by(Expense.category)
        for category, total in session.execute(statement):
            print(f"{category}: {total}")
finally:
    engine.dispose()
