# Independent task: methods, invariants & state changes
#
# Define Account(balance) requiring a nonnegative plain-integer starting balance. Define
# withdraw(amount) requiring a positive plain integer no greater than the current balance. Raise
# ValueError before changing state for any invalid value; otherwise subtract the amount and
# return the new balance. Start at 100, withdraw 30, then attempt to withdraw 80. Print the
# balance after success, Rejected for ValueError, and the actual balance afterward. A rejected
# withdrawal must leave state unchanged.
#
# Expected output:
#
# 70
# Rejected
# 70

