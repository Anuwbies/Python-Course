# Independent task: transactions & consistent changes
#
# Implement transfer(connection, source, destination, amount) using bound SQL and a single
# connection transaction. Require a positive plain integer amount and distinct IDs. Debit only
# when balance is sufficient; reject a zero-row debit or destination update with ValueError.
# Seed account 1 with 100 and account 2 with 0. Transfer 30 from 1 to 2, then attempt 10 from 1
# to missing account 99. Print actual ordered balances after each operation and Rejected between
# them.
#
# Expected output:
#
# [70, 30]
# Rejected
# [70, 30]

