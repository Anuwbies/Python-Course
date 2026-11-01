# Independent task: exception contracts & interchangeable stages
#
# Define InvalidAmount as a ValueError subtype. Define parse_amount(text), converting integer
# text, translating conversion ValueError to InvalidAmount with an explicit cause, and rejecting
# negative results with InvalidAmount. Print parse_amount("12"). For parse_amount("tea"), catch
# InvalidAmount and print the type name of its explicit cause.
#
# Expected output:
#
# 12
# ValueError

