# Independent task: composition & dependency injection
#
# Define MemoryStore with save/load methods for lists of integers; both boundaries must copy the
# outer list. Define ExpenseService(store) with total() using store.load(). Save [120, 80],
# create the service, and print its total. Modify a loaded copy by appending 999 and print the
# total again; it must remain unchanged.
#
# Expected output:
#
# 200
# 200

