# Independent task: request validation & response contracts
#
# Implement an isolated in-memory create_app() with POST /orders and GET /orders/{order_id}.
# Define OrderInput with whitespace-stripped item text of length 1..80, a strict plain-integer
# quantity from 1 through 100, and forbidden extra fields. Define OrderOutput with those fields
# plus an integer id. Then assign increasing IDs from 1 under a shared Lock, return 201 on
# creation, 404 for missing IDs, and use an output model including id/item/quantity. Demonstrate
# a valid creation, a Boolean quantity rejection, and a missing read; print the three response
# statuses.
#
# Expected output:
#
# 201
# 422
# 404

