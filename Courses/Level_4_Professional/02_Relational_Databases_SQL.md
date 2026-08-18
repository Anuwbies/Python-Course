# Lesson 2: Relational Databases & Raw SQL with PostgreSQL

Enterprise applications require durable, relational data storage with ACID guarantees.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Connect to PostgreSQL using modern asynchronous drivers (`asyncpg`).
2. Manage connection pooling to support thousands of concurrent queries.
3. Write parameterized SQL queries to prevent **SQL Injection**.
4. Handle database transactions and rollbacks.

---

## 1. Async PostgreSQL with Connection Pools (`asyncpg`)

```python
import asyncio
import asyncpg

async def main():
    # Establish a connection pool
    pool = await asyncpg.create_pool(
        user="postgres",
        password="secretpassword",
        database="production_db",
        host="localhost",
        min_size=5,
        max_size=20
    )

    async with pool.acquire() as conn:
        # Create table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                balance NUMERIC(10, 2) NOT NULL DEFAULT 0.00
            );
        """)

        # Parameterized query (Prevents SQL Injection!)
        await conn.execute(
            "INSERT INTO accounts (username, balance) VALUES ($1, $2) ON CONFLICT DO NOTHING;",
            "alex_dev", 500.00
        )

        # Query records
        row = await conn.fetchrow("SELECT * FROM accounts WHERE username = $1;", "alex_dev")
        print(f"Account: {row['username']} | Balance: ${row['balance']}")

    await pool.close()

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 📝 Quick Exercise

**Prompt**:
Write an async SQL transaction that transfers money between two accounts atomically, rolling back if the sender has insufficient funds.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import asyncpg

async def transfer_funds(pool: asyncpg.Pool, from_user: str, to_user: str, amount: float):
    async with pool.acquire() as conn:
        # Open transaction block: commits on clean exit, rolls back on error
        async with conn.transaction():
            # Check balance with row locking (FOR UPDATE)
            sender = await conn.fetchrow("SELECT balance FROM accounts WHERE username = $1 FOR UPDATE;", from_user)
            if not sender or sender['balance'] < amount:
                raise ValueError("Insufficient funds or invalid sender account!")
            
            await conn.execute("UPDATE accounts SET balance = balance - $1 WHERE username = $2;", amount, from_user)
            await conn.execute("UPDATE accounts SET balance = balance + $1 WHERE username = $2;", amount, to_user)
            print("Transfer completed atomically! 💸")
```
</details>
