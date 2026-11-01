# Independent task: safer saves & cleanup
#
# Define save_amounts(path, amounts) for a list of plain nonnegative integers. Validate and
# serialize before touching the destination. Write the JSON to a unique NamedTemporaryFile in
# the destination directory, close it, replace the destination, and remove a leftover temporary
# file in finally. In an isolated directory save [10], attempt to save [-1] and catch
# ValueError, then read and print the actual destination contents as parsed JSON.
#
# Expected output:
#
# Invalid save rejected
# [10]

