# Independent task: cancellation, timeouts & task groups
#
# Define async work(events) that awaits a long cooperative sleep and appends closed in finally.
# In main, await it inside asyncio.timeout(0), catch TimeoutError outside, print Timed out, and
# then print whether events equals ["closed"]. The cleanup must be real, not a fixed success
# flag.
#
# Expected output:
#
# Timed out
# Cleaned up: True

