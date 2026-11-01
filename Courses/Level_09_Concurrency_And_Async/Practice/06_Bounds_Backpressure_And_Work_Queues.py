# Independent task: bounds, backpressure & work queues
#
# Define async run_bounded(values, limit) for positive integer limit. Use a semaphore around
# each operation, track active and maximum active counts in event-loop-owned state, yield with
# sleep(0), and return input-order doubled results plus the observed maximum. Print results for
# [1,2,3] at limit 2 and whether the maximum was at most 2. Reject a nonpositive limit with
# ValueError.
#
# Expected output:
#
# [2, 4, 6]
# Within limit: True

