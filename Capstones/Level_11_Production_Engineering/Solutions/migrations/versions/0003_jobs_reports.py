from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("jobs", sa.Column("id",sa.String(36),primary_key=True),
        sa.Column("request_key",sa.String(80),nullable=False,unique=True),
        sa.Column("status",sa.String(10),nullable=False),
        sa.Column("attempts",sa.Integer(),nullable=False),
        sa.Column("last_error",sa.String(80),nullable=True),
        sa.Column("created_at",sa.DateTime(timezone=True),nullable=False,server_default=sa.func.now()),
        sa.CheckConstraint("attempts BETWEEN 0 AND 3",name="ck_jobs_attempts"),
        sa.CheckConstraint("status IN ('pending','done','failed')",name="ck_jobs_status"))
    op.create_table("reports",sa.Column("job_id",sa.String(36),sa.ForeignKey("jobs.id"),primary_key=True),sa.Column("body",sa.Text(),nullable=False))

def downgrade():
    op.drop_table("reports")
    op.drop_table("jobs")
