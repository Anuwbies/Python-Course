# Lesson 7: Records, Aggregation & Reports

**Prerequisites:** Level 1 and Lessons 1–6 of this level. **Practice file:** `Practice/07_Records_Aggregation_And_Reports.py`.

Combine collections without losing the meaning of individual records. A report is a deliberate reduction of data: preserve the entries, group them by an explicit rule, and display a stable summary.

## 1. Give each record a consistent shape

A list of dictionaries can hold an ordered collection of expenses. Every record should use the same field names and units. A field named amount should not mean pesos in one record and centavos in another.

```python
expenses = [
    {"category": "food", "amount": 120},
    {"category": "travel", "amount": 30},
    {"category": "food", "amount": 80},
]
print(expenses[0]["amount"])  # 120
```

The first lookup selects a record from the list; the second selects a field from that record. These are two separate relationships. Use clear intermediate names when a longer expression makes this distinction difficult to see.

## 2. Reduce records into totals

Initialize an overall total and a category dictionary before the loop. Each record contributes once to the overall total and once to its category. The category dictionary is an output being built, not a replacement for the original history.

```python
expenses = [{"category": "food", "amount": 120}, {"category": "food", "amount": 80}]
total = 0
by_category = {}
for expense in expenses:
    category = expense["category"]
    amount = expense["amount"]
    total = total + amount
    by_category[category] = by_category.get(category, 0) + amount
print(total)                # 200
print(by_category["food"])  # 200
```

An empty expense list naturally produces zero and an empty grouping dictionary. You do not need to invent a fake zero-valued record to make the report work. Be careful not to reset by_category inside the loop, which would discard earlier groups.

## 3. Normalize only the intended fields

Category labels entered by users can include spaces or different letter case. A deliberate rule such as `.strip().lower()` can group `" FOOD "` with `"food"`. Apply it at entry or in aggregation consistently. Do not silently apply the same rule to a person's display name if preserving their spelling matters.

The input assumptions still matter: these records contain nonnegative integer amounts. Conditions can reject a negative amount when it is entered. Handling a nonnumeric response with recovery remains a later topic.

For whitespace-separated text, `text.split()` returns a list of words split on runs of whitespace. With no separator argument it drops surrounding whitespace and empty gaps. It does not remove punctuation, so a tokenization policy must state whether `food` and `food,` mean the same thing.

## 4. Make report order explicit

`sorted(by_category)` returns a new list of keys in sorted order. Visit those keys and look up each corresponding value. This makes a report independent of the order in which categories first appeared.

Do not sort the original history merely to display a summary unless changing history order is intended. A new summary is a different representation of the same facts. When investigating a wrong total, compare the sum of category totals with the overall total; disagreement often means a record was skipped, duplicated, or grouped using the wrong amount.

References: [Python data structures](https://docs.python.org/3.13/tutorial/datastructures.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Calculate the grouped totals by hand for three records with a repeated category.
2. **Explain:** Explain why one dictionary can summarize many original records.
3. **Modify:** Normalize labels with outer whitespace and mixed case before grouping.
4. **Debug:** Find the initialization that was mistakenly placed inside the aggregation loop.

<details>
<summary>Hints</summary>

Build the totals first and print afterward; sorted supplies the category order.

</details>

## Independent task: records, aggregation & reports

In `Practice/07_Records_Aggregation_And_Reports.py`, complete this task:

Use the records `{"category": "food", "amount": 120}`, `{"category": "travel", "amount": 30}`, and `{"category": "food", "amount": 80}` in a list. Calculate the overall total and category totals. Print the total first, followed by category totals in alphabetical category order.

Expected output:

```text
Total: PHP 230
food: PHP 200
travel: PHP 30
```
