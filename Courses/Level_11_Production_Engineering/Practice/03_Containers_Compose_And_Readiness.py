# Independent task: containers, compose & readiness
#
# Implement copy_assets(destination) to copy Dockerfile, compose.yaml, requirements.txt,
# service.py, and .dockerignore from this level's Assets directory into an existing or newly
# created destination. Use pathlib and shutil.copyfile; return the sorted copied names.
# Demonstrate copying to a TemporaryDirectory and print the names. The copied Compose stack must
# later be run with Docker to establish runtime health; the Python demonstration reports files
# only.
#
# Expected output:
#
# ['.dockerignore', 'Dockerfile', 'compose.yaml', 'requirements.txt', 'service.py']

