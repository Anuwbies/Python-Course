# Independent task: authentication, tokens & authorization
#
# Use pwdlib.PasswordHash.recommended to hash and verify an example password, printing True for
# the correct value and False for a wrong one. Generate an ephemeral key with
# secrets.token_urlsafe(32). Issue a five-minute HS256 JWT for sub=mika and role=reader with
# iat/exp/aud=course-api/iss=course-issuer. Decode with an explicit algorithm allowlist,
# required claims, audience and issuer, validate the custom subject/role, and print the verified
# role. Do not print the password hash, key, or token.
#
# Expected output:
#
# True
# False
# reader

