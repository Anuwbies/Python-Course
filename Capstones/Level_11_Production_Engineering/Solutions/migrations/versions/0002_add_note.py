from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("orders", sa.Column("note", sa.String(120), nullable=False, server_default=""))
    with op.batch_alter_table("orders") as batch:
        batch.create_check_constraint("ck_orders_note", "length(note) <= 120")

def downgrade():
    with op.batch_alter_table("orders") as batch:
        batch.drop_constraint("ck_orders_note", type_="check")
        batch.drop_column("note")
