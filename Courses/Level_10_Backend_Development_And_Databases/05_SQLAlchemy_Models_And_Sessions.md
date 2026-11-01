# Lesson 5: SQLAlchemy Models & Sessions

**Prerequisites:** Levels 1–9 and Lessons 1–4 of this level. **Practice file:** `Practice/05_SQLAlchemy_Models_And_Sessions.py`.

Use an ORM to map objects to relational rows while retaining explicit transaction and query boundaries. An ORM reduces repetitive mapping work; it does not remove SQL behavior or database constraints.

## 1. Declare the mapping

SQLAlchemy 2.0 uses DeclarativeBase, Mapped annotations, and mapped_column for an explicit typed mapping. A class's table name and columns describe storage; constraints remain database rules rather than Python-only assertions.

```python
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = (CheckConstraint("amount >= 0"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    amount: Mapped[int]
```

The empty Base class intentionally selects the ORM's base behavior; it is not an unfinished exercise. The Mapped annotations participate in mapping configuration. They do not by themselves validate arbitrary external request payloads.

## 2. Separate engine and session

An engine owns database connectivity and pooling behavior. A Session tracks object changes and a transaction. Use a fresh appropriately scoped session for a request or unit of work rather than one global mutable session shared by unrelated callers.

`session.add` stages a new object. Flush sends pending statements within the transaction; commit finishes the transaction. A failed flush leaves the session needing rollback before reuse. A session context closes its resources, while a begin context can also express commit/rollback scope.

## 3. Query only what is needed

Use select with explicit ordering and projections. `session.scalars(select(Expense))` yields mapped objects; selecting category and aggregate values yields row results. An ORM relationship accessed lazily can issue additional queries, so a short property-looking expression may hide repeated database work.

For a grouped report, ask the database to group and sum when that matches the workload. Loading every row into Python merely to calculate a simple aggregate can waste memory and transfer. Measure rather than assuming object mapping is always the bottleneck.

## 4. Distinguish initialization from migration

`Base.metadata.create_all(engine)` creates missing tables in a demonstration database. It is not a schema migration system and does not evolve existing columns automatically. The next lesson introduces explicit revisions.

SQLite in-memory connection/thread behavior differs from a persistent file. A database that appears empty from another connection may be a different in-memory instance. The capstone uses a file database and explicit migrations to demonstrate persistence across application factories.

## Run the ORM query through a concrete session

The Expense mapping above needs an actual engine, schema, and session before it can persist anything:

```python
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

# Expense and Base are the mapping declared earlier in this lesson.
engine = create_engine("sqlite+pysqlite:///:memory:")
try:
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        with session.begin():
            session.add_all([Expense(category="books", amount=25),
                             Expense(category="books", amount=15)])
        statement = (select(Expense.category, func.sum(Expense.amount))
                     .group_by(Expense.category).order_by(Expense.category))
        for category, total in session.execute(statement):
            print(category, total)  # books 40
finally:
    engine.dispose()
```

add_all stages several objects. The begin block commits on normal exit and rolls back on an escaping error. func builds database function expressions; group_by and order_by append clauses rather than mutating caller records. dispose releases the engine's pooled connections; it is separate from closing one Session.

`select(Expense).where(Expense.id == identifier)` adds a filter. `session.get(Expense, identifier)` retrieves by primary key or returns None. `session.scalar(statement)` returns the first selected scalar or None; `session.execute(statement).one()` requires exactly one result row; `.scalar_one()` requires exactly one scalar. These methods have different empty/multiple-result contracts. After a committed insert, `session.refresh(object)` reloads generated fields when needed; `session.rollback()` resets a failed transaction before another query.

`mapped_column(String(80), nullable=False, unique=True)` explicitly describes text storage, nullability, and uniqueness; import String from sqlalchemy. `ForeignKey("parents.id")` declares a reference, Text is unbounded text storage, and DateTime(timezone=True) requests a time-aware database column. Python-side `default=callable` runs when SQLAlchemy inserts, whereas `server_default=...` belongs to the database schema. A class body containing only pass is intentionally empty syntax, not an unfinished practice marker.

References: [SQLAlchemy 2.0 tutorial](https://docs.sqlalchemy.org/en/20/tutorial/).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict whether add necessarily commits immediately.
2. **Explain:** Explain the responsibilities of an engine versus a session.
3. **Modify:** Project only category and a sum for a grouped report.
4. **Debug:** Find a claim that create_all upgrades an existing schema.

<details>
<summary>Hints</summary>

Keep the session local to the unit of work and perform the aggregation in the query.

</details>

## Independent task: sqlalchemy models & sessions

In `Practice/05_SQLAlchemy_Models_And_Sessions.py`, complete this task:

Define an Expense ORM model with id, category, amount and a nonnegative amount CHECK constraint. In a real isolated in-memory SQLite engine, create the demonstration schema, insert food/120, food/80, travel/30 in a transaction, and query category sums with SQLAlchemy select/func.sum/group_by/order_by. Print alphabetical labeled totals and dispose the engine.

Expected output:

```text
food: 200
travel: 30
```
