# Accepted inputs: nonempty name, nonnegative integer amounts, positive days.
# Read each response in the same order as the capstone brief.
print("Name:")
name = input().strip()
print("Weekly budget (whole PHP):")
budget = int(input())
print("Study days:")
days = int(input())
print("Daily transport (whole PHP):")
daily_transport = int(input())
print("Daily food (whole PHP):")
daily_food = int(input())
print("Other weekly costs (whole PHP):")
other_weekly = int(input())

# Daily costs occur on every study day. Other costs are already weekly.
weekly_transport = daily_transport * days
weekly_food = daily_food * days
planned_spending = weekly_transport + weekly_food + other_weekly
remaining = budget - planned_spending

# Spending averages and allocations of available money answer different questions.
average_planned = planned_spending / days
whole_daily_budget = budget // days
unallocated = budget % days

# Format the report; keep the calculated values numeric.
print()
print("WEEKLY BUDGET")
print(f"Name: {name}")
print(f"Budget: PHP {budget}")
print(f"Days: {days}")
print(f"Transport: PHP {weekly_transport}")
print(f"Food: PHP {weekly_food}")
print(f"Other: PHP {other_weekly}")
print(f"Planned spending: PHP {planned_spending}")
print(f"Remaining: PHP {remaining}")
print(f"Average planned per day: PHP {average_planned:.2f}")
print(f"Whole-peso daily budget: PHP {whole_daily_budget}")
print(f"Unallocated from daily split: PHP {unallocated}")
