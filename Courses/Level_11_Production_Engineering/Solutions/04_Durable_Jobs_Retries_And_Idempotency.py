import sqlite3
from contextlib import closing

def enqueue(connection, key, amount):
    if not isinstance(key, str) or not key.strip() or type(amount) is not int or amount < 0:
        raise ValueError("Invalid job")
    with connection:
        connection.execute("INSERT OR IGNORE INTO jobs(key,amount,status,attempts) VALUES (?,?,'pending',0)", (key,amount))
        row = connection.execute("SELECT amount FROM jobs WHERE key=?", (key,)).fetchone()
        if row[0] != amount:
            raise ValueError("Key reused with different payload")
    return key

def process(connection, key, fail=False):
    row = connection.execute("SELECT amount,status,attempts FROM jobs WHERE key=?", (key,)).fetchone()
    if row is None:
        raise KeyError(key)
    amount, status, attempts = row
    if status == "done":
        return False
    if attempts >= 3:
        raise RuntimeError("Attempt limit reached")
    with connection:
        connection.execute("UPDATE jobs SET attempts=attempts+1 WHERE key=?", (key,))
    with connection:
        connection.execute("INSERT INTO receipts(key,amount) VALUES (?,?)", (key,amount))
        if fail:
            raise RuntimeError("Simulated local failure")
        connection.execute("UPDATE jobs SET status='done' WHERE key=?", (key,))
    return True

if __name__ == "__main__":
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript("CREATE TABLE jobs(key TEXT PRIMARY KEY,amount INTEGER NOT NULL CHECK(amount >= 0),status TEXT NOT NULL CHECK(status IN ('pending','done','failed')),attempts INTEGER NOT NULL CHECK(attempts BETWEEN 0 AND 3)); CREATE TABLE receipts(key TEXT PRIMARY KEY REFERENCES jobs(key),amount INTEGER NOT NULL);")
        enqueue(connection, "request-1", 120)
        try:
            process(connection, "request-1", fail=True)
        except RuntimeError:
            print("Attempt failed")
        process(connection, "request-1")
        print(f"Receipts: {connection.execute('SELECT COUNT(*) FROM receipts').fetchone()[0]}")
        print(f"Replay performed work: {process(connection, 'request-1')}")
