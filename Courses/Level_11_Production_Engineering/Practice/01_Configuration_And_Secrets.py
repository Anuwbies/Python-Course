# Independent task: configuration & secrets
#
# Define load_settings(mapping) returning a frozen Settings with database_url (excluded from its
# generated repr) and token_ttl_seconds. Require nonblank DATABASE_URL and an integer
# TOKEN_TTL_SECONDS from 1 through 3600, raising ValueError with a setting name on invalid
# input. Demonstrate a valid mapping with TTL 300 and an invalid zero TTL. Print the valid TTL
# and Rejected; do not print the database URL.
#
# Expected output:
#
# 300
# Rejected

