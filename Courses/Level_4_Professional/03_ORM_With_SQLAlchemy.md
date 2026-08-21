# Lesson 3: Modern ORM with SQLAlchemy 2.0 & Async Engine

Writing raw SQL strings in application code can become brittle and error-prone as schemas evolve. **Object-Relational Mapping (ORM)** bridges relational database tables and Python classes. **SQLAlchemy 2.0** is the industry standard for Python ORMs, featuring declarative type annotations (`Mapped`, `mapped_column`), fully asynchronous query execution (`AsyncSession`), and prevention of the infamous $\mathcal{O}(N+1)$ query trap via eager loading (`selectinload`).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Model database schemas using modern **SQLAlchemy 2.0 Declarative Mappings** (`Mapped`, `mapped_column`).
2. Establish One-to-Many and Many-to-Many relationships with `relationship()` and `back_populates`.
3. Configure the **Async SQLAlchemy Engine** (`create_async_engine`, `async_sessionmaker`).
4. Execute type-safe asynchronous queries using the 2.0 `select()` syntax.
5. Eliminate the **N+1 Query Problem** using eager loading (`selectinload`).
6. Manage ACID database transaction lifecycles using `async with session.begin():`.

---

## 1. Modern SQLAlchemy 2.0 Declarative Models

In SQLAlchemy 2.0, models inherit from `DeclarativeBase` and use standard Python type annotations:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import List

class Base(DeclarativeBase):
    pass

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    # One-to-Many relationship
    employees: Mapped[List["Employee"]] = relationship(back_populates="company", cascade="all, delete-orphan")

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)

    # Many-to-One back reference
    company: Mapped["Company"] = relationship(back_populates="employees")
```

---

## 2. The Async Engine & Session Lifecycle

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# SQLite async connection string requires sqlite+aiosqlite://
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        # Create all tables asynchronously
        await conn.run_sync(Base.metadata.create_all)
```

---

---

## 4. Under the Hood: Unit of Work & Identity Map

SQLAlchemy `Session` implements the **Unit of Work** and **Identity Map** patterns:
- **Identity Map**: Keeps track of every loaded Python object by primary key (`(Company, 1)`). Multiple queries for the same primary key return the exact same Python instance in memory (`obj1 is obj2`), eliminating duplicate objects.
- **Unit of Work**: Changes made to objects (`user.email = "new@corp.com"`) are tracked in memory without sending immediate SQL. When `session.commit()` is called, SQLAlchemy computes the minimal topological diff and flushes changes in an optimized batch.

---

## 5. Many-to-Many Relationships & Association Tables

```python
from sqlalchemy import Table, Column, Integer, ForeignKey

# Dedicated Association Table (stores purely linking foreign keys):
user_role_association = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    roles: Mapped[List["Role"]] = relationship(secondary=user_role_association, back_populates="users")

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    users: Mapped[List["User"]] = relationship(secondary=user_role_association, back_populates="roles")
```

---

## 6. Connection Pool Configuration for Production

```python
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/prod_db",
    pool_size=20,          # Persistent baseline connection count
    max_overflow=10,       # Temporary surge capacity
    pool_recycle=1800,     # Recycle connections after 30 mins to avoid dropped sockets
    pool_pre_ping=True,    # Test connections before checkout (eliminates stale socket errors)
)
```

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master SQLAlchemy 2.0 declarative models, async querying, relations, and eager loading:

---

### 🟢 Tier 1: Declarative Models & Async CRUD (Exercises 1–3)

#### 🔹 Exercise 1: Single Model Declaration
* **Goal**: Define `Product(Base)` with `id`, `sku`, and `price` using `Mapped` and `mapped_column`.

#### 🔹 Exercise 2: Async Table Creation & Add Record
* **Goal**: Initialize an async SQLite memory database and insert a new product within `async with session.begin():`.

#### 🔹 Exercise 3: Type-Safe Async Select
* **Goal**: Query products with `select(Product).where(Product.price > 50.0)` using `scalars().all()`.

---

### 🟡 Tier 2: Relationships & Cascades (Exercises 4–6)

#### 🔹 Exercise 4: One-to-Many Bidirectional Relationship
* **Goal**: Build `Author` and `Book` models with `relationship(back_populates="...")`.

#### 🔹 Exercise 5: Cascade Orphan Deletion
* **Goal**: Configure `cascade="all, delete-orphan"` on child records and verify child rows are deleted when removed from list.

#### 🔹 Exercise 6: Many-to-Many Association
* **Goal**: Build `Student` and `Course` models connected via `secondary=association_table`.

---

### 🟠 Tier 3: Eager Loading & Complex Async Queries (Exercises 7–9)

#### 🔹 Exercise 7: Eliminate N+1 with `selectinload`
* **Goal**: Load 10 authors and all their books in 2 optimized SQL queries using `selectinload(Author.books)`.

#### 🔹 Exercise 8: Joined Eager Loading with `joinedload`
* **Goal**: Query single orders with their customer details using `joinedload(Order.customer)`.

#### 🔹 Exercise 9: Async Aggregations & Grouping
* **Goal**: Write an async `select(Department.name, func.count(Employee.id)).group_by(...)` query.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Customer Support Helpdesk ORM Engine
* **Goal**: Model a multi-tiered helpdesk support ticket database with async session transactions and eager ticket loading.

---

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Multi-Tenant SaaS Organization & Team Membership Engine**, demonstrating modern SQLAlchemy 2.0 models, async session transactions, eager relationship loading, and cascading record deletion:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Multi-Tenant Enterprise SaaS Team Membership Engine
# =====================================================================

import asyncio
from typing import List
from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# 1. SQLAlchemy 2.0 Declarative Models (Lesson 3)
class Base(DeclarativeBase):
    pass

class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    org_slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    plan_tier: Mapped[str] = mapped_column(String(20), default="ENTERPRISE")

    # One-to-Many: An Organization has many User Memberships
    members: Mapped[List["Member"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan"
    )

class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="DEVELOPER")
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)

    # Many-to-One back reference
    organization: Mapped["Organization"] = relationship(back_populates="members")


# 2. Async Database Engine Setup
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


# 3. Database Operations & Query Execution
async def populate_sample_tenant_data():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            org1 = Organization(org_slug="apex-ai", name="Apex AI Research Labs", plan_tier="ENTERPRISE")
            org2 = Organization(org_slug="cloud-scale", name="CloudScale Global Ltd", plan_tier="PRO")

            m1 = Member(email="elena.rostova@apex.ai", full_name="Elena Rostova", role="CHIEF_ARCHITECT", organization=org1)
            m2 = Member(email="marcus.vance@apex.ai", full_name="Marcus Vance", role="LEAD_SRE", organization=org1)
            m3 = Member(email="sarah.connor@cloudscale.io", full_name="Sarah Connor", role="HEAD_OF_ENG", organization=org2)

            session.add_all([org1, org2, m1, m2, m3])


async def query_tenant_directory():
    async with AsyncSessionLocal() as session:
        # Optimized query with selectinload to fetch organizations and their members eagerly
        stmt = (
            select(Organization)
            .options(selectinload(Organization.members))
            .order_by(Organization.name)
        )
        result = await session.execute(stmt)
        organizations = result.scalars().all()

        print("=" * 80)
        print(f"{'ENTERPRISE MULTI-TENANT SAAS DIRECTORY (SQLALCHEMY 2.0)':^80}")
        print("=" * 80)

        for org in organizations:
            print(f"\n🏢 Organization: {org.name} [{org.org_slug}] - Plan: {org.plan_tier}")
            print(f"   Active Team Members ({len(org.members)}):")
            for member in org.members:
                print(f"     • {member.full_name:<20} | Role: {member.role:<18} | Email: {member.email}")

        print("\n" + "=" * 80)


# 4. Master Async Execution Runner
async def main():
    # Create tables in memory
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await populate_sample_tenant_data()
    await query_tenant_directory()
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
```

### 🔍 Code Explanation:
- **`Mapped[T]` & `mapped_column()`**: Employs modern SQLAlchemy 2.0 type annotations that integrate cleanly with IDEs, mypy, and type checkers.
- **`selectinload(Organization.members)`**: Eagerly fetches related member collections using an optimized secondary query, preventing async relationship loading runtime errors.
- **`cascade="all, delete-orphan"`**: Deleting an organization automatically purges its associated members without leaving orphan rows in the database.

---

## 📝 Quick Exercise: E-Commerce Customer & Support Ticket Management ORM

### 🏢 Real-Life Scenario
You are developing the Customer Support Ticket management backend for an e-commerce platform. The system models customers (`Customer`) and their submitted helpdesk tickets (`SupportTicket`). You must define the SQLAlchemy 2.0 models, establish a One-to-Many relationship, seed sample tickets, and execute an async query fetching all open tickets for a customer.

### 📋 Requirements
1. **Define `Customer` Model**:
   - `id: Mapped[int] = mapped_column(primary_key=True)`
   - `email: Mapped[str] = mapped_column(String(255), unique=True)`
   - `full_name: Mapped[str] = mapped_column(String(100))`
   - `tickets: Mapped[List["SupportTicket"]] = relationship(back_populates="customer")`
2. **Define `SupportTicket` Model**:
   - `id: Mapped[int] = mapped_column(primary_key=True)`
   - `subject: Mapped[str] = mapped_column(String(200))`
   - `priority: Mapped[str] = mapped_column(String(20))` (e.g. `"CRITICAL"`, `"HIGH"`, `"LOW"`)
   - `status: Mapped[str] = mapped_column(String(20), default="OPEN")`
   - `customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))`
   - `customer: Mapped["Customer"] = relationship(back_populates="tickets")`
3. Seed a customer with 2 tickets (one `"OPEN"`, one `"RESOLVED"`).
4. Execute an async `select()` with `selectinload(Customer.tickets)` and print the ticket manifest.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 4 SQLAlchemy 2.0 and AsyncEngine with Level 3 asyncio, Level 2 OOP, and Level 1 string formatting.

### 🎯 Expected Output
```text
==================================================
       CUSTOMER SUPPORT HELPDESK ORM REPORT       
==================================================
Customer: Elena Rostova (elena@enterprise.com)
Total Tickets Logged: 2
--------------------------------------------------
TICKETS:
  - [OPEN]     Priority: CRITICAL | Order delivery delayed past ETA
  - [RESOLVED] Priority: LOW      | Request invoice copy for Q2
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Helpdesk ORM & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Customer Support Helpdesk ORM Engine
# =====================================================================
import asyncio
from typing import List
from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    full_name: Mapped[str] = mapped_column(String(100))
    tickets: Mapped[List["SupportTicket"]] = relationship(back_populates="customer")

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String(200))
    priority: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20), default="OPEN")
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship(back_populates="tickets")


async def run_support_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            c = Customer(email="elena@enterprise.com", full_name="Elena Rostova")
            t1 = SupportTicket(subject="Order delivery delayed past ETA", priority="CRITICAL", status="OPEN", customer=c)
            t2 = SupportTicket(subject="Request invoice copy for Q2", priority="LOW", status="RESOLVED", customer=c)
            session.add_all([c, t1, t2])

    async with async_session() as session:
        stmt = select(Customer).options(selectinload(Customer.tickets))
        res = await session.execute(stmt)
        cust = res.scalars().first()

        print("==================================================")
        print("       CUSTOMER SUPPORT HELPDESK ORM REPORT       ")
        print("==================================================")
        print(f"Customer: {cust.full_name} ({cust.email})")
        print(f"Total Tickets Logged: {len(cust.tickets)}")
        print("--------------------------------------------------")
        print("TICKETS:")
        for t in cust.tickets:
            print(f"  - [{t.status:<8}] Priority: {t.priority:<8} | {t.subject}")
        print("==================================================")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(run_support_engine())

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: Product Model
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True)
    price: Mapped[float]

# Ex 2: Async Add
# async with session.begin(): session.add(Product(sku="P1", price=10.0))

# Ex 3: Select Where
# stmt = select(Product).where(Product.price > 50.0); res = await session.scalars(stmt)

# Ex 4: One-to-Many
# class Author(Base): books: Mapped[List["Book"]] = relationship(back_populates="author")

# Ex 5: Orphan Cascade
# children: Mapped[List["Child"]] = relationship(cascade="all, delete-orphan")

# Ex 6: Many-to-Many
# roles: Mapped[List["Role"]] = relationship(secondary=user_roles)

# Ex 7: selectinload
# select(Author).options(selectinload(Author.books))

# Ex 8: joinedload
# from sqlalchemy.orm import joinedload
# select(Order).options(joinedload(Order.customer))

# Ex 9: Group By Aggregations
# from sqlalchemy import func
# select(Department.name, func.count(Employee.id)).group_by(Department.name)
```
</details>
