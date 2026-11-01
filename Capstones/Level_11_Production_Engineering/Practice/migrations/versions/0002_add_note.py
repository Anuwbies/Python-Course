# Independent task: note revision 0002
#
# Set revision="0002", down_revision="0001", branch_labels=None, depends_on=None. Upgrade adds
# orders.note as nonnullable String(120) with an empty server default, then creates
# ck_orders_note requiring length(note)<=120 using batch_alter_table. Downgrade drops
# ck_orders_note and note in a batch context.
#
# Expected behavior: existing orders retain id/item/quantity and receive an empty note;
# downgrade preserves those base fields while discarding note data.

