# Independent task: jobs and reports revision 0003
#
# Set revision="0003", down_revision="0002", branch_labels=None, depends_on=None. Upgrade
# creates jobs with id String(36) primary key, unique nonnullable request_key String(80),
# nonnullable status String(10), nonnullable attempts Integer, nullable last_error String(80),
# and nonnullable created_at DateTime(timezone=True) with func.now() server default. Add
# ck_jobs_attempts for attempts BETWEEN 0 AND 3 and ck_jobs_status for status IN
# ('pending','done','failed'). Application inserts supply id/status/attempts through the ORM
# defaults.
#
# Create reports with job_id String(36) primary key referencing jobs.id and nonnullable body
# Text. Downgrade drops reports before jobs.
#
# Expected behavior: head is 0003, one report can exist per job, and downgrade to 0002 preserves
# orders.

