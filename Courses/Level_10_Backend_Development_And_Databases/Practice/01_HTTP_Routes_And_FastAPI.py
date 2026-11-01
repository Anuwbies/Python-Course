# Independent task: http, routes & fastapi
#
# Define create_app() returning a FastAPI application with GET /health -> {"status":"ok"} and
# GET /double/{value} accepting an integer and returning {"result": value*2}. In a guarded
# TestClient demonstration, request /double/3 and print its HTTP status and result. Use the real
# response, not fixed status values.
#
# Expected output:
#
# 200
# 6

