from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import Column, String, create_engine, inspect, text

engine = create_engine("sqlite+pysqlite:///:memory:")
try:
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE orders (id INTEGER PRIMARY KEY, quantity INTEGER NOT NULL)"))
        connection.execute(text("INSERT INTO orders VALUES (1, 2)"))
        operations = Operations(MigrationContext.configure(connection))
        operations.add_column("orders", Column("note", String(120), nullable=False, server_default=""))
        print("note" in [column["name"] for column in inspect(connection).get_columns("orders")])
        print(connection.execute(text("SELECT quantity FROM orders WHERE id = 1")).scalar_one())
        with operations.batch_alter_table("orders") as batch:
            batch.drop_column("note")
        print("note" in [column["name"] for column in inspect(connection).get_columns("orders")])
finally:
    engine.dispose()
