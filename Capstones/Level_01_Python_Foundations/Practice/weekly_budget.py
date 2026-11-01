# Capstone task: weekly budget calculator
#
# Write an interactive program that reads a student's budget and planned costs,
# calculates the weekly spending, and displays a report using the actual values.
#
# Read these six responses in order. Print each prompt on its own line before
# reading its response:
# 1. Name:
# 2. Weekly budget (whole PHP):
# 3. Study days:
# 4. Daily transport (whole PHP):
# 5. Daily food (whole PHP):
# 6. Other weekly costs (whole PHP):
#
# Assume the name is nonempty after surrounding whitespace is removed, all
# money amounts are nonnegative whole-peso integers, and study days is a
# positive integer. Clean the name and convert the five numeric responses
# to integers. Preserve meaningful internal spaces and accents in the name.
#
# Calculate:
# - Weekly transport: daily transport multiplied by study days.
# - Weekly food: daily food multiplied by study days.
# - Planned spending: weekly transport plus weekly food plus other weekly costs.
# - Remaining: weekly budget minus planned spending. Keep negative results.
# - Average planned per day: planned spending divided by study days.
# - Whole-peso daily budget: weekly budget floor-divided by study days.
# - Unallocated from daily split: the remainder of weekly budget divided by days.
#
# Count other weekly costs once. Keep the calculations numeric and display the
# average with two decimal places. Use only Level 1 concepts: no conditions,
# loops, custom functions, imports, classes, or exception handling.
#
# Sample input, one response per line:
# Mika
# 1000
# 5
# 40
# 100
# 150
#
# Expected program output, excluding the typed responses:
# Name:
# Weekly budget (whole PHP):
# Study days:
# Daily transport (whole PHP):
# Daily food (whole PHP):
# Other weekly costs (whole PHP):
#
# WEEKLY BUDGET
# Name: Mika
# Budget: PHP 1000
# Days: 5
# Transport: PHP 200
# Food: PHP 500
# Other: PHP 150
# Planned spending: PHP 850
# Remaining: PHP 150
# Average planned per day: PHP 170.00
# Whole-peso daily budget: PHP 200
# Unallocated from daily split: PHP 0

