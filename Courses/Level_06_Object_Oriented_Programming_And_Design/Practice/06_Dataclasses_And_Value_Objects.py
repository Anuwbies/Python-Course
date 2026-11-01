# Independent task: dataclasses & value objects
#
# Define a frozen dataclass Expense with category:str and amount:int. In post-init reject a
# blank category or an amount whose type is not exactly int or is negative, using ValueError.
# Construct food/120 and print its fields as one line. Attempt food/True and print Rejected for
# ValueError.
#
# Expected output:
#
# food 120
# Rejected

