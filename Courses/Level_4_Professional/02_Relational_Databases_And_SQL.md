# Lesson 2: Relational Database Design & SQL Engineering

No backend software exists in isolation—relational database management systems (RDBMS) such as PostgreSQL and SQLite form the persistent backbone of enterprise platforms. In this lesson, you will master relational schema design, SQL Data Definition (DDL) and Manipulation (DML), complex relational `JOIN` operations, database indexing, ACID transactions, and parameterized SQL queries to eradicate SQL Injection vulnerabilities.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Design normalized relational schemas with Primary Keys, Foreign Keys, and Unique Constraints.
2. Write production SQL queries including `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.
3. Join related tables across one-to-many and many-to-many relationships using `INNER JOIN` and `LEFT JOIN`.
4. Perform data aggregation using `COUNT()`, `SUM()`, `AVG()`, `GROUP BY`, and `HAVING`.
5. Understand **ACID Transaction Guarantees** and prevent SQL Injection using **Parameterized Queries**.

---

## 1. Relational Schema Architecture (DDL)

```sql
-- Users Table (One-to-Many with Orders)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders Table (Child table with Foreign Key constraint)
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexing for fast search
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

---

## 2. Relational JOINs & Aggregations (DML)

```sql
-- Fetch all users alongside their total aggregated spend:
SELECT 
    u.id,
    u.full_name,
    COUNT(o.id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0.00) AS lifetime_value
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.full_name
HAVING COUNT(o.id) > 0
ORDER BY lifetime_value DESC;
```

---

---

## 4. ACID Transaction Guarantees & Isolation Levels

| Principle | Description | Mechanism |
| :--- | :--- | :--- |
| **Atomicity** | All statements execute completely or all changes roll back. | Undo Logs / Savepoints |
| **Consistency** | Database transitions only between valid states satisfying constraints. | Schema Foreign Key & Unique Checks |
| **Isolation** | Concurrent transactions execute without mutual interference. | MVCC (Multi-Version Concurrency Control) / Locks |
| **Durability** | Committed transactions survive power loss or crashes. | WAL (Write-Ahead Logging) to disk |

### Isolation Levels & Anomalies
1. **Read Uncommitted**: Suffers from *Dirty Reads* (reading uncommitted data).
2. **Read Committed** (Default in PostgreSQL): Prevents dirty reads; suffers from *Non-Repeatable Reads*.
3. **Repeatable Read**: Prevents non-repeatable reads; snapshots row versions.
4. **Serializable**: Strict serial ordering; prevents all concurrency anomalies including *Phantom Reads*.

---

## 5. B-Tree Indexes & Composite Index Rules

- **B-Tree Index**: Automatically created for `PRIMARY KEY` and `UNIQUE` columns. Provides $\mathcal{O}(\log n)$ equality and range searches.
- **Leftmost Prefix Rule**: A composite index on `(last_name, first_name)` accelerates queries on `last_name` alone, but **cannot** accelerate queries filtering solely on `first_name`.

---

## 6. SQL Window Functions (`OVER (PARTITION BY ... ORDER BY ...)`)

Window functions calculate running totals and rankings across partitions without collapsing rows like `GROUP BY`:

```sql
SELECT 
    employee_id,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary
FROM employees;
```

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master SQL DDL/DML, relational joins, ACID transactions, window functions, and indexing:

---

### 🟢 Tier 1: Schema DDL & Basic CRUD (Exercises 1–3)

#### 🔹 Exercise 1: Table Creation with Constraints
* **Goal**: Write DDL creating `products` with `CHECK (price > 0)` and `UNIQUE(sku)`.

#### 🔹 Exercise 2: Parameterized Batch Insert
* **Goal**: Insert 10 user rows using `cursor.executemany("INSERT INTO ... VALUES (?, ?)", rows)`.

#### 🔹 Exercise 3: Filter & Sorting Queries
* **Goal**: Select active users with `status = 'ACTIVE'` ordered by `created_at DESC` with `LIMIT 10`.

---

### 🟡 Tier 2: Relational JOINs & Aggregations (Exercises 4–6)

#### 🔹 Exercise 4: Inner vs Left Outer Join
* **Goal**: Fetch all customers including those who have never placed an order using `LEFT JOIN`.

#### 🔹 Exercise 5: Group By and Having Filter
* **Goal**: Find all departments with total payroll budget exceeding $\$500,000$ using `HAVING SUM(salary) > 500000`.

#### 🔹 Exercise 6: Cascade Deletion Foreign Keys
* **Goal**: Verify that deleting a parent user row automatically cascades to delete all child orders in SQLite with `PRAGMA foreign_keys = ON;`.

---

### 🟠 Tier 3: ACID Transactions & Window Analytics (Exercises 7–9)

#### 🔹 Exercise 7: Atomic Multi-Account Wire Transfer
* **Goal**: Execute a debit and credit within a single SQL transaction, triggering `conn.rollback()` on insufficient balance.

#### 🔹 Exercise 8: Ranking with Window Functions
* **Goal**: Assign `DENSE_RANK()` to students ordered by test score per classroom `PARTITION BY classroom_id`.

#### 🔹 Exercise 9: SQL Query Execution Plan (`EXPLAIN QUERY PLAN`)
* **Goal**: Run `EXPLAIN QUERY PLAN` on an unindexed query (Scan Table) vs indexed query (Search Table using Index).

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Academic Registrar GPA Engine
* **Goal**: Build a multi-table university grading database computing student credit-weighted GPAs with relational JOIN aggregations.

---

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise E-Commerce Order Fulfillment & Inventory Management Database Engine**, demonstrating schema creation, foreign key enforcement, parameterized batch inserts, multi-table `JOIN` aggregations, and ACID transaction rollbacks using Python's `sqlite3`:

```python
# =====================================================================
# REAL-WORLD SYSTEM: E-Commerce Inventory & Order Relational Database
# =====================================================================

import sqlite3
import os

DB_FILE = "ecommerce_store.db"

# Remove existing database file if present
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# Connect to database (enabling Foreign Key constraints)
conn = sqlite3.connect(DB_FILE)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

# 1. Schema Definition (Lesson 2 DDL)
cursor.executescript("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    tier TEXT DEFAULT 'STANDARD'
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    price REAL NOT NULL,
    stock_units INTEGER NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")
conn.commit()

# 2. Seed Data via Parameterized Queries
customers_data = [
    ("elena.rostova@enterprise.com", "Elena Rostova", "VIP"),
    ("marcus.vance@tech.io", "Marcus Vance", "STANDARD"),
    ("sarah.connor@cyber.org", "Sarah Connor", "VIP"),
]
cursor.executemany("INSERT INTO customers (email, full_name, tier) VALUES (?, ?, ?)", customers_data)

products_data = [
    ("SKU-LAPTOP", "Pro UltraBook 16-inch", 1499.00, 20),
    ("SKU-MONITOR", "4K HDR IPS Monitor", 450.00, 15),
    ("SKU-MOUSE", "Ergonomic Bluetooth Mouse", 60.00, 50),
]
cursor.executemany("INSERT INTO products (sku, title, price, stock_units) VALUES (?, ?, ?, ?)", products_data)
conn.commit()


# 3. ACID Transactional Order Placement Engine
def place_order_transaction(customer_id: int, items_to_buy: list[tuple[int, int]]) -> int:
    """Places an order atomically: updates stock, creates order and line items.
    
    Rolls back automatically on any inventory or database failure.
    """
    try:
        total_order_amount = 0.0
        validated_items = []

        # Validate stock and compute totals
        for prod_id, qty in items_to_buy:
            cursor.execute("SELECT title, price, stock_units FROM products WHERE product_id = ?", (prod_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Product ID {prod_id} does not exist.")
            title, price, stock = row
            if stock < qty:
                raise ValueError(f"Insufficient stock for '{title}' (Requested: {qty}, Available: {stock})")
            
            line_total = price * qty
            total_order_amount += line_total
            validated_items.append((prod_id, qty, price))

        # Insert Master Order
        cursor.execute(
            "INSERT INTO orders (customer_id, total_amount) VALUES (?, ?)",
            (customer_id, total_order_amount)
        )
        new_order_id = cursor.lastrowid

        # Insert Line Items & Deduct Inventory Stock
        for prod_id, qty, price in validated_items:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (new_order_id, prod_id, qty, price)
            )
            cursor.execute(
                "UPDATE products SET stock_units = stock_units - ? WHERE product_id = ?",
                (qty, prod_id)
            )

        conn.commit() # Commit atomic transaction
        return new_order_id

    except Exception as err:
        conn.rollback() # Rollback all partial writes
        raise err


# Place successful order
order_1 = place_order_transaction(customer_id=1, items_to_buy=[(1, 1), (2, 2)]) # Laptop + 2 Monitors

# 4. Multi-Table Relational Reporting Query
cursor.execute("""
SELECT 
    c.full_name AS customer,
    c.tier,
    o.order_id,
    p.title AS product,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS line_total,
    o.total_amount AS order_total
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id;
""")

rows = cursor.fetchall()

print("=" * 85)
print(f"{'E-COMMERCE RELATIONAL DATABASE REPORT (MULTI-TABLE JOIN)':^85}")
print("=" * 85)
print(f"{'Customer':<18} | {'Tier':<8} | {'Order ID':<8} | {'Product Title':<25} | {'Qty':>3} | {'Line Total':>10}")
print("-" * 85)
for r in rows:
    cust, tier, o_id, prod, qty, price, line_tot, ord_tot = r
    print(f"{cust:<18} | {tier:<8} | #{o_id:<7} | {prod:<25} | {qty:>3} | ${line_tot:>9,.2f}")
print("-" * 85)

conn.close()
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
```

### 🔍 Code Explanation:
- **Foreign Key Cascade & PRAGMA**: `PRAGMA foreign_keys = ON;` forces SQLite to validate parent row existence across foreign keys.
- **ACID Transaction Block**: `place_order_transaction` checks inventory availability, inserts orders, writes line items, and deducts inventory inside a single atomic transaction wrapped in `conn.commit()` and `conn.rollback()`.
- **4-Table Relational JOIN**: Demonstrates connecting `customers`, `orders`, `order_items`, and `products` to produce a single consolidated customer billing view.

---

## 📝 Quick Exercise: University Student Course Registration & GPA Relational Engine

### 🏢 Real-Life Scenario
You are developing the academic records database for a university registrar. The database manages students, academic courses, and course enrollments with letter grades. You must construct the relational schema, insert sample enrollment records using parameterized SQL, and execute an aggregation query computing each student's Grade Point Average (GPA).

### 📋 Requirements
1. **Create SQLite Relational Schema**:
   - `students (student_id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE)`
   - `courses (course_id INTEGER PRIMARY KEY, course_code TEXT UNIQUE, credits INTEGER)`
   - `enrollments (enrollment_id INTEGER PRIMARY KEY, student_id INTEGER, course_id INTEGER, grade_points REAL, FOREIGN KEY ...)`
2. **Insert Seed Data**:
   - Students: Elena (ID 1), Marcus (ID 2).
   - Courses: CS101 (4 credits), MATH201 (3 credits), PHYS101 (4 credits).
   - Enrollments:
     - Elena: CS101 (Grade: 4.0), MATH201 (Grade: 3.7)
     - Marcus: CS101 (Grade: 3.0), PHYS101 (Grade: 3.3)
3. **Execute GPA Aggregation Query**:
   - Calculates weighted GPA: $\frac{\sum(\text{grade\_points} \times \text{credits})}{\sum(\text{credits})}$.
   - Groups by `student_id` and student `name`.
4. Output the student GPA transcript table.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 4 SQL schema design, parameterized inserts, and `JOIN` aggregations with Level 1 loops and string formatting.

### 🎯 Expected Output
```text
==================================================
       UNIVERSITY ACADEMIC REGISTRAR REPORT       
==================================================
Student Name         | Courses Taken | Credits |   GPA
--------------------------------------------------
Elena Rostova        |             2 |       7 |  3.87
Marcus Vance         |             2 |       8 |  3.15
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Registrar & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: University Academic Registrar GPA Engine
# =====================================================================
import sqlite3
import os

DB_NAME = "university_registry.db"
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT UNIQUE NOT NULL,
    credits INTEGER NOT NULL
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade_points REAL NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
""")
conn.commit()

cursor.executemany(
    "INSERT INTO students (name, email) VALUES (?, ?)",
    [("Elena Rostova", "elena@uni.edu"), ("Marcus Vance", "marcus@uni.edu")]
)

cursor.executemany(
    "INSERT INTO courses (course_code, credits) VALUES (?, ?)",
    [("CS101", 4), ("MATH201", 3), ("PHYS101", 4)]
)

cursor.executemany(
    "INSERT INTO enrollments (student_id, course_id, grade_points) VALUES (?, ?, ?)",
    [
        (1, 1, 4.0),
        (1, 2, 3.7),
        (2, 1, 3.0),
        (2, 3, 3.3),
    ]
)
conn.commit()

cursor.execute("""
SELECT 
    s.name,
    COUNT(e.enrollment_id) AS total_courses,
    SUM(c.credits) AS total_credits,
    ROUND(SUM(e.grade_points * c.credits) / SUM(c.credits), 2) AS weighted_gpa
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id
GROUP BY s.student_id, s.name
ORDER BY weighted_gpa DESC;
""")

results = cursor.fetchall()

print("==================================================")
print("       UNIVERSITY ACADEMIC REGISTRAR REPORT       ")
print("==================================================")
print(f"{'Student Name':<20} | {'Courses Taken':>13} | {'Credits':>7} | {'GPA':>5}")
print("-" * 50)
for name, num_courses, credits, gpa in results:
    print(f"{name:<20} | {num_courses:>13} | {credits:>7} | {gpa:>5.2f}")
print("==================================================")

conn.close()
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: Schema Constraints
# CREATE TABLE products (id INTEGER PRIMARY KEY, sku TEXT UNIQUE, price REAL CHECK(price > 0));

# Ex 2: Parameterized Batch Insert
# cursor.executemany("INSERT INTO users (email) VALUES (?)", [("a@b.com",), ("c@d.com",)])

# Ex 3: Filter & Sort
# cursor.execute("SELECT * FROM users WHERE status = 'ACTIVE' ORDER BY created_at DESC LIMIT 10")

# Ex 4: Left Join
# cursor.execute("SELECT u.id, o.id FROM users u LEFT JOIN orders o ON u.id = o.user_id")

# Ex 5: Group By & Having
# cursor.execute("SELECT dept, SUM(salary) FROM emp GROUP BY dept HAVING SUM(salary) > 500000")

# Ex 6: Cascade Deletion
# FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

# Ex 7: Transaction Rollback
# try: conn.execute(...); conn.commit() except Exception: conn.rollback()

# Ex 8: Window Rank
# SELECT id, dept, salary, DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) FROM emp

# Ex 9: EXPLAIN QUERY PLAN
# cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'test@example.com'")
```
</details>
