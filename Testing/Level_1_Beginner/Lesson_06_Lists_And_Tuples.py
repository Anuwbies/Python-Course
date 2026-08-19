"""
================================================================================
Level 1: Beginner Python
Lesson 6: Lists & Tuples
================================================================================
📝 Quick Exercise: Warehouse Inventory Fulfillment Analytics

🏢 Real-Life Scenario:
You are developing the weekly logistics and demand forecasting report for an
e-commerce fulfillment warehouse. The operations team tracks daily shipped unit
counts for a flagship consumer electronic SKU across the 7 days of the operational
week. The system must analyze sales volume, identify peak and lowest volume days,
isolate above-average fulfillment spikes, and project next week's initial restock
requirement.

📋 Requirements:
1. Declare weekly data collections:
   - weekly_sales = [145, 230, 180, 310, 260, 420, 195]
   - day_names = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
2. Compute statistical aggregates:
   - total_units = sum(weekly_sales)
   - days_count = len(weekly_sales)
   - average_daily_units = total_units / days_count
   - max_units = max(weekly_sales)
   - min_units = min(weekly_sales)
   - peak_day_name, lowest_day_name using .index()
3. Use a list comprehension to extract above_average_sales.
4. Use .copy() and .append() to project next day demand (int(average_daily_units * 1.15)).
5. Print a daily shipment ledger and summary report.

⚠️ Strict Constraint:
Use ONLY concepts covered in Lessons 1-6 (variables, primitives, input(), numbers,
strings, conditionals, loops, range(), lists, tuples, indexing, slicing, list
methods, list comprehensions, aggregate functions, f-strings, and print()).
No dictionaries, sets, or functions.
================================================================================
"""

# 1. Declare weekly data collections
weekly_sales = [145, 230, 180, 310, 260, 420, 195]
day_names = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

# 2. Compute aggregate metrics
total_units = sum(weekly_sales)
days_count = len(weekly_sales)
average_daily_units = total_units / days_count
max_units = max(weekly_sales)
min_units = min(weekly_sales)

peak_day_index = weekly_sales.index(max_units)
peak_day_name = day_names[peak_day_index]

lowest_day_index = weekly_sales.index(min_units)
lowest_day_name = day_names[lowest_day_index]

# 3. List comprehension for above-average days
above_average_sales = [units for units in weekly_sales if units > average_daily_units]

# 4. Projected demand with copy and append
projected_target = int(average_daily_units * 1.15)
restock_projection = weekly_sales.copy()
restock_projection.append(projected_target)

# 5. Output formatted report
print("==================================================")
print("      WAREHOUSE WEEKLY FULFILLMENT REPORT         ")
print("==================================================")
print("DAILY SHIPMENT LEDGER:")
for i in range(len(weekly_sales)):
    print(f"- {day_names[i]:<9}: {weekly_sales[i]} units")

print("--------------------------------------------------")
print("WEEKLY PERFORMANCE METRICS:")
print(f"Total Volume:       {total_units:,} units")
print(f"Daily Average:      {average_daily_units:.2f} units/day")
print(f"Peak Fulfillment:   {peak_day_name} ({max_units} units)")
print(f"Lowest Fulfillment: {lowest_day_name} ({min_units} units)")
print("--------------------------------------------------")
print(f"High Volume Days (>Avg): {above_average_sales} ({len(above_average_sales)} days)")
print(f"Next Day Projected Need: {projected_target} units")
print("==================================================")