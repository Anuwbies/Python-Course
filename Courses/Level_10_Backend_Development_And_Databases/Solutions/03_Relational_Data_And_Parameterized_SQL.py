import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:")) as connection:
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
    connection.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), quantity INTEGER NOT NULL CHECK (quantity > 0))")
    with connection:
        connection.executemany("INSERT INTO customers VALUES (?, ?)", [(1, "Mika"), (2, "José")])
        connection.executemany("INSERT INTO orders VALUES (?, ?, ?)", [(1, 1, 1), (2, 1, 2), (3, 2, 1)])
    rows = connection.execute("SELECT c.name, SUM(o.quantity) FROM customers AS c JOIN orders AS o ON o.customer_id = c.id GROUP BY c.id, c.name ORDER BY c.name")
    for name, total in rows:
        print(f"{name}: {total}")
