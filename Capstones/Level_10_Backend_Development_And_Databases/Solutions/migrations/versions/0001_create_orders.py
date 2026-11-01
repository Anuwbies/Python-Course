from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("orders", sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("item", sa.String(80), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.CheckConstraint("quantity BETWEEN 1 AND 100", name="ck_orders_quantity"),
        sa.CheckConstraint("length(trim(item)) BETWEEN 1 AND 80", name="ck_orders_item"))

def downgrade():
    op.drop_table("orders")
