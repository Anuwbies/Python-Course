# Prompts are separate print calls so reading and displaying are explicit.
print("Name:")
name = input().strip()
print("Days:")
days = int(input())
print("Budget (whole PHP):")
budget = int(input())

# The task assumes positive days and a nonnegative whole-peso budget.
daily_budget = budget / days

print(f"Hello, {name}.")
print(f"Days: {days}")
print(f"Budget: PHP {budget}")
print(f"Daily budget: PHP {daily_budget:.2f}")
