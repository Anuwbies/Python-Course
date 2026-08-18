# Lesson 3: SQLAlchemy 2.0 Async ORM & Data Modeling

SQLAlchemy 2.0 is the industry standard Object-Relational Mapper (ORM) for Python, providing a type-safe bridge between Python objects and relational database tables.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Define Declarative Base Models with type-annotated `Mapped` fields.
2. Establish One-to-Many and Many-to-Many relationships.
3. Prevent the **N+1 Query Problem** with eager loading (`selectinload`).
4. Integrate SQLAlchemy async sessions into FastAPI endpoints.

---

## 1. Defining Models with SQLAlchemy 2.0

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Numeric
from typing import List

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100))

    # One-to-Many relationship
    orders: Mapped[List["Order"]] = relationship(back_populates="customer", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    customer: Mapped["Customer"] = relationship(back_populates="orders")
```

---

## 2. Preventing the N+1 Query Problem

When fetching 100 customers and accessing their orders, lazy loading issues 101 queries. Eager loading solves this in **2 queries**:

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# Eager loads all orders in an optimized single secondary query:
stmt = select(Customer).options(selectinload(Customer.orders))
```

---

## 📝 Quick Exercise

**Prompt**:
Create a Many-to-Many relationship between `Student` and `Course` via an association table `enrollments`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

# Association Table
enrollments = Table(
    "enrollments",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    courses: Mapped[list["Course"]] = relationship(secondary=enrollments, back_populates="students")

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    students: Mapped[list["Student"]] = relationship(secondary=enrollments, back_populates="courses")
```
</details>
