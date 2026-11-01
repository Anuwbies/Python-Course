# Independent task: descriptors & class creation
#
# Implement Nonnegative with set_name/get/set, requiring a plain nonnegative integer and
# preserving the old value on rejection. Class access returns the descriptor; an uninitialized
# instance read raises AttributeError. Implement FieldMeta(type) collecting directly declared
# Nonnegative attribute names into field_names. Define Account(metaclass=FieldMeta) with balance
# and an initializer assigning it. Print Account.field_names, a starting balance of 100,
# Rejected after assigning -1, and the unchanged balance.
#
# Expected output:
#
# ('balance',)
# 100
# Rejected
# 100

