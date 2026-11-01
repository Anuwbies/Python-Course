# Independent task: orders revision 0001
#
# Set revision="0001", down_revision=None, branch_labels=None, depends_on=None. Upgrade creates
# orders: id Integer primary key, item nonnullable String(80), quantity nonnullable Integer. Add
# named checks ck_orders_quantity for quantity BETWEEN 1 AND 100 and ck_orders_item for
# length(trim(item)) BETWEEN 1 AND 80. Downgrade drops orders. Use real Alembic op operations.
#
# Expected behavior: upgrade to 0001 creates the base table without note; downgrade removes that
# table.

