import sqlite3
from time import perf_counter_ns

def health_snapshot(connection):
    start = perf_counter_ns()
    try:
        connection.execute("SELECT COUNT(*) FROM orders").fetchone()
    except sqlite3.Error:
        ready = False
    else:
        ready = True
    return {"ready": ready, "duration_ns": perf_counter_ns() - start}

connection = sqlite3.connect(":memory:")
connection.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY)")
print(health_snapshot(connection)["ready"])
connection.close()
print(health_snapshot(connection)["ready"])
