# Lesson 3: Relational Data & Parameterized SQL

**Prerequisites:** Levels 1–9 and Lessons 1–2 of this level. **Practice file:** `Practice/03_Relational_Data_And_Parameterized_SQL.py`.

Define relationships and constraints in the database, then use parameters for values. SQL is a declarative language for selecting and changing relational data, not a string-formatting substitute for validation.

## 1. Identify entities and relationships

A customer table can identify customers by a primary key. An orders table refers to that key through a foreign key. This avoids repeating all customer details in every order and gives the relationship an explicit referential rule.

SQLite is included through sqlite3 and is suitable for local relational exercises. Enable foreign_keys on each connection when relying on its foreign-key enforcement. A declared constraint that is not enabled in the connection's environment cannot protect the intended relationship.

## 2. Parameterize values

```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:")) as connection:
    connection.execute("CREATE TABLE amounts (amount INTEGER NOT NULL CHECK (amount >= 0))")
    connection.execute("INSERT INTO amounts(amount) VALUES (?)", (120,))
    print(connection.execute("SELECT amount FROM amounts").fetchone()[0])
```

The placeholder receives a bound value; the one-element tuple needs its comma. Do not use an f-string to splice untrusted text into a SQL statement. Parameters represent values, not arbitrary table or column identifiers; identifier selection needs a separate controlled policy.

## 3. Join and aggregate deliberately

A JOIN combines rows according to a relationship. GROUP BY partitions rows for aggregates such as SUM. ORDER BY establishes display order; SQL results without it should not be treated as having a guaranteed report order.

An inner join excludes a customer with no matching orders. A left join can retain that customer, producing null values for missing joined data; COALESCE can supply a chosen report value for a null aggregate. Those choices express different questions and should be intentional.

## 4. Separate transaction scope and connection lifetime

A sqlite3 connection context manager commits or rolls back a transaction, but does not itself close the connection. contextlib.closing is a small manager that closes its object on exit. Use it around the connection and a transaction block when both responsibilities are needed.

Constraints complement application validation because every database writer should follow the same essential rules. A quantity CHECK does not replace a full domain workflow, and transaction boundaries remain important when several valid statements must succeed together.

## Build a relationship and execute a grouped query

This complete example uses teams and scores to make the SQL syntax visible before applying it to customers and orders:

```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:")) as connection:
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("CREATE TABLE teams (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
    connection.execute("CREATE TABLE scores (team_id INTEGER NOT NULL REFERENCES teams(id), points INTEGER NOT NULL CHECK (points > 0))")
    with connection:
        connection.execute("INSERT INTO teams VALUES (?, ?)", (1, "Blue"))
        connection.executemany("INSERT INTO scores VALUES (?, ?)", [(1, 2), (1, 3)])
    statement = "SELECT t.name, SUM(s.points) FROM teams AS t JOIN scores AS s ON s.team_id = t.id GROUP BY t.id, t.name ORDER BY t.name"
    for name, total in connection.execute(statement):
        print(name, total)  # Blue 5
```

PRIMARY KEY identifies a row; NOT NULL forbids a missing value; REFERENCES links to an existing row; CHECK constrains each stored value. executemany runs one parameterized statement for each supplied tuple. AS introduces a short table alias, ON states the join relationship, GROUP BY selects the grouping identity, and ORDER BY fixes result order. `fetchone()` returns one result tuple or None; a cursor can also be iterated for all rows.

UPDATE changes rows selected by WHERE and can calculate from existing column values, such as `SET points = points + ? WHERE team_id = ?`. DELETE removes selected rows. SQL COUNT counts rows; COALESCE substitutes a chosen value for NULL. SQL BETWEEN includes both limits and IN tests membership in listed values. Functions such as length(trim(name)) can express a nonblank bounded text CHECK. Keep identifiers controlled and continue binding all external values.

References: [SQLite3 interface](https://docs.python.org/3.13/library/sqlite3.html), [SQLite SQL language](https://www.sqlite.org/lang.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict whether an inner join includes a customer with no orders.
2. **Explain:** Explain why a bound parameter is different from formatted SQL text.
3. **Modify:** Add ORDER BY to make a grouped report deterministic.
4. **Debug:** Find a connection that was committed but never closed.

<details>
<summary>Hints</summary>

Create the relationship, bind the sample values, then group rows by the customer identity.

</details>

## Independent task: relational data & parameterized sql

In `Practice/03_Relational_Data_And_Parameterized_SQL.py`, complete this task:

Create isolated in-memory customers and orders tables. Enable foreign keys, require positive quantities, and insert Mika with quantities 1 and 2 and José with quantity 1 using bound values. Query the summed quantity per customer through a JOIN and GROUP BY, ordered by customer name, and print `<name>: <total>`. Close the connection.

Expected output:

```text
José: 1
Mika: 3
```
