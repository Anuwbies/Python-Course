# Task: implement revision 0002 with down_revision="0001".
# Upgrade adds nonnullable note String(120) with an empty server default, preserving
# existing records, and a named length(note) <= 120 CHECK constraint using batch DDL.
# Downgrade drops that constraint and column using batch_alter_table.
# Expected behavior: head includes note; downgrade to 0001 preserves base rows.

