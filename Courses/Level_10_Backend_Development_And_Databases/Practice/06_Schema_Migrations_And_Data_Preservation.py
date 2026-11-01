# Independent task: schema migrations & data preservation
#
# Create a real in-memory orders table containing id 1 and quantity 2. Use Alembic
# MigrationContext/Operations to add a nonnullable string note column with an empty server
# default. Print whether note exists and the preserved quantity. Use batch_alter_table to drop
# note, then print whether it still exists. Dispose the engine.
#
# Expected output:
#
# True
# 2
# False

