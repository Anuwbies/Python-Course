# Task: implement revision 0001 with down_revision=None.
# Upgrade creates orders with integer primary-key id, nonnullable item String(80),
# quantity Integer, and named CHECK constraints quantity BETWEEN 1 AND 100 and
# length(trim(item)) BETWEEN 1 AND 80. Downgrade drops orders.
# Expected behavior: revision 0001 creates the base schema without a note field.

