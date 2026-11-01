# Independent task: issue_token.py
#
# Implement an operator-only argparse command requiring --subject and --role reader/admin. Read
# a
# configured TOKEN_SECRET of at least 32 characters; issue a five-minute HS256 JWT with sub,
# role,
# iat, exp, aud=course-api, iss=course-issuer using UTC timestamps. Print only the token. Do not
# expose this command as an unauthenticated API route. Expected behavior: the token grants
# exactly
# its verified role until expiry.

