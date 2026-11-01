# Independent task: sqlalchemy models & sessions
#
# Define an Expense ORM model with id, category, amount and a nonnegative amount CHECK
# constraint. In a real isolated in-memory SQLite engine, create the demonstration schema,
# insert food/120, food/80, travel/30 in a transaction, and query category sums with SQLAlchemy
# select/func.sum/group_by/order_by. Print alphabetical labeled totals and dispose the engine.
#
# Expected output:
#
# food: 200
# travel: 30

