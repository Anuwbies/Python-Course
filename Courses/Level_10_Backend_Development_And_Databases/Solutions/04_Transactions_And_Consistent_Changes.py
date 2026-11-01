import sqlite3
from contextlib import closing

def transfer(connection, source, destination, amount):
    if type(amount) is not int or amount <= 0 or source == destination:
        raise ValueError("Invalid transfer")
    with connection:
        changed = connection.execute("UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?", (amount, source, amount))
        if changed.rowcount != 1:
            raise ValueError("Source missing or insufficient balance")
        changed = connection.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, destination))
        if changed.rowcount != 1:
            raise ValueError("Destination missing")

if __name__ == "__main__":
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER NOT NULL CHECK (balance >= 0))")
        with connection:
            connection.executemany("INSERT INTO accounts VALUES (?, ?)", [(1,100),(2,0)])
        transfer(connection, 1, 2, 30)
        print([row[0] for row in connection.execute("SELECT balance FROM accounts ORDER BY id")])
        try:
            transfer(connection, 1, 99, 10)
        except ValueError:
            print("Rejected")
        print([row[0] for row in connection.execute("SELECT balance FROM accounts ORDER BY id")])
