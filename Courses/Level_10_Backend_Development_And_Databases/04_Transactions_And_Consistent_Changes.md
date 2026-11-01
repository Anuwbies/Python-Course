# Lesson 4: Transactions & Consistent Changes

**Prerequisites:** Levels 1–9 and Lessons 1–3 of this level. **Practice file:** `Practice/04_Transactions_And_Consistent_Changes.py`.

Make several related database changes succeed or fail together. A transaction boundary protects a data invariant; it does not replace deciding which statements and validation belong inside that boundary.

## 1. Group related statements

A transfer debits one balance and credits another. If the credit fails after a committed debit, the data no longer expresses the intended transfer. Run both statements in one transaction and allow a failure to roll back the group.

With sqlite3, a connection context manager commits on normal exit and rolls back when an exception leaves the block. Do not catch an error inside the block and then proceed as if everything succeeded; the context may see a normal exit and commit the partial change.

## 2. Check the operation's actual effect

An UPDATE can execute successfully while affecting zero rows. A conditional debit can use `WHERE id = ? AND balance >= ?` and inspect rowcount to distinguish a completed update from an unmet condition. This avoids a separate unprotected read-then-write sequence for that particular rule.

The task reports a missing source or insufficient balance as a documented ValueError. A different API may distinguish them further, but neither case should be presented as a successful transfer. Check the destination update too.

## 3. Keep failure before commit

```text
# A transaction-shaped outline; the operations must raise on failure.
def transfer(connection, source, destination, amount):
    with connection:
        debit(connection, source, amount)
        credit(connection, destination, amount)
```

The outline names collaborators for explanation; the independent task implements the actual bound SQL statements. A later failure must propagate out of the transaction block for rollback. A success message belongs after the block commits, not after only the first statement.

## 4. Understand the boundary's limits

Transaction isolation and locking differ across database systems and settings. A local SQLite transaction does not establish a general distributed transaction across a payment service, queue, and database. External effects may need an outbox or idempotent recovery design later.

Avoid holding a transaction open while waiting for unrelated network input. Keep its scope aligned with the invariant, and handle retries only under a clearly understood failure policy. Repeating a non-idempotent operation after an ambiguous outcome can duplicate effects.

To demonstrate rollback, inspect the actual data after the rejected operation. Printing rolled back inside an except block is not evidence that the first update was undone.

References: [SQLite transaction control](https://docs.python.org/3.13/library/sqlite3.html#transaction-control).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict balances when a destination is absent after the debit statement.
2. **Explain:** Explain why catching a failure inside the transaction can change commit behavior.
3. **Modify:** Inspect affected-row counts for both updates.
4. **Debug:** Move a success message to after the transaction has completed.

<details>
<summary>Hints</summary>

Let the destination failure leave the transaction block before handling it.

</details>

## Independent task: transactions & consistent changes

In `Practice/04_Transactions_And_Consistent_Changes.py`, complete this task:

Implement transfer(connection, source, destination, amount) using bound SQL and a single connection transaction. Require a positive plain integer amount and distinct IDs. Debit only when balance is sufficient; reject a zero-row debit or destination update with ValueError. Seed account 1 with 100 and account 2 with 0. Transfer 30 from 1 to 2, then attempt 10 from 1 to missing account 99. Print actual ordered balances after each operation and Rejected between them.

Expected output:

```text
[70, 30]
Rejected
[70, 30]
```
