budget = 503
people = 4

# Equal whole units and the units left unallocated are different results.
whole_share = budget // people
leftover = budget % people
reconstructed_total = whole_share * people + leftover

print(whole_share)
print(leftover)
print(reconstructed_total)
