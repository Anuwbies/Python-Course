# Lesson 7: Dictionaries & Sets

In this lesson, you will master Python's two fundamental hash-based data structures: **Dictionaries** (key-value associative maps) and **Sets** (unique element collections). Both structures provide near-instantaneous $O(1)$ data access and lookup capabilities.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Store and manipulate structured key-value pairs in Dictionaries `{key: value}`.
2. Understand hash tables, constant-time $O(1)$ lookups, and key hashability requirements.
3. Access values safely using `.get()` and `.setdefault()` to prevent `KeyError` crashes.
4. Iterate over dictionary keys, values, and `(key, value)` tuple pairs using `.items()`.
5. Eliminate duplicate data instantly using Sets `{...}`.
6. Execute mathematical set operations: Union (`|`), Intersection (`&`), Difference (`-`), and Symmetric Difference (`^`).
7. Write concise **Dictionary Comprehensions**.

---

## 1. Dictionaries: Key-Value Hash Maps

A **dictionary** is an unordered (insertion-ordered in Python 3.7+), mutable collection of key-value pairs. Instead of numeric index offsets, you access values via descriptive keys.

```python
# Defining a dictionary:
server_node = {
    "hostname": "prod-api-01",
    "ip_address": "192.168.1.105",
    "cpu_cores": 16,
    "ram_gb": 64.0,
    "is_active": True,
    "active_ports": [80, 443, 8080]
}

# 1. Accessing values:
print(server_node["hostname"])    # 'prod-api-01'
print(server_node["ram_gb"])      # 64.0

# 2. Modifying existing values:
server_node["ram_gb"] = 128.0

# 3. Adding new key-value pairs:
server_node["region"] = "us-east-1"

# 4. Deleting keys:
del server_node["is_active"]
removed_ports = server_node.pop("active_ports")  # Removes key and returns its value
```

### 🔑 Key Hashability Rules
- **Dictionary keys MUST be immutable (hashable)**: Strings, integers, floats, and tuples can be keys.
- **Lists and dictionaries CANNOT be keys** (raises `TypeError: unhashable type: 'list'`).

---

## 2. Safe Retrieval with `.get()` & `.setdefault()`

Accessing a non-existent key using bracket syntax `dict[key]` raises a fatal `KeyError`. The `.get()` method prevents crashes by returning a fallback default value:

```python
config = {"theme": "dark", "font_size": 14}

# Risky direct access:
# print(config["volume"])  # ❌ KeyError: 'volume'

# Safe access with .get(key, default_fallback):
volume = config.get("volume", 50)       # Returns 50 because "volume" is not found
theme = config.get("theme", "light")     # Returns "dark" (key exists)

print(f"Volume: {volume} | Theme: {theme}")
```

### Frequency Counting Pattern with `.get()`:
```python
votes = ["Alice", "Bob", "Alice", "Charlie", "Alice", "Bob"]
vote_counts = {}

for candidate in votes:
    # If candidate not in dict, start at 0 and add 1
    vote_counts[candidate] = vote_counts.get(candidate, 0) + 1

print(vote_counts)  # {'Alice': 3, 'Bob': 2, 'Charlie': 1}
```

---

## 3. Iterating Over Dictionaries

```python
stock = {"Laptops": 15, "Monitors": 42, "Keyboards": 85}

# 1. Iterate over keys:
for item in stock.keys():
    print(f"Product: {item}")

# 2. Iterate over values:
for qty in stock.values():
    print(f"Quantity on hand: {qty}")

# 3. Iterate over key-value pairs (Standard Idiom):
for product, quantity in stock.items():
    print(f"- {product:<12}: {quantity:>3} units")
```

---

## 4. Sets: Unique, Hash-Based Collections

A **set** is an unordered collection of unique elements enclosed in `{...}` (or created with `set()`). Sets automatically deduplicate input data.

```python
raw_user_roles = ["admin", "editor", "guest", "editor", "admin", "viewer"]
unique_roles = set(raw_user_roles)

print(unique_roles)  # {'admin', 'editor', 'guest', 'viewer'}
```

> [!NOTE]
> To create an empty set, you **must** use `set()`. `{}` creates an empty dictionary!

---

## 5. Mathematical Set Operations

Sets provide built-in operators for Venn-diagram style mathematical set logic:

```python
frontend_devs = {"Alice", "Bob", "Charlie", "Diana"}
backend_devs  = {"Charlie", "Diana", "Evan", "Frank"}

# 1. Union (|): Members in EITHER set (Combined team)
all_engineers = frontend_devs | backend_devs
# {'Alice', 'Bob', 'Charlie', 'Diana', 'Evan', 'Frank'}

# 2. Intersection (&): Members in BOTH sets (Full-stack devs)
full_stack = frontend_devs & backend_devs
# {'Charlie', 'Diana'}

# 3. Difference (-): In frontend_devs but NOT in backend_devs
pure_frontend = frontend_devs - backend_devs
# {'Alice', 'Bob'}

# 4. Symmetric Difference (^): In ONE set only, but NOT in both
single_specialty = frontend_devs ^ backend_devs
# {'Alice', 'Bob', 'Evan', 'Frank'}
```

---

## 6. Dictionary Comprehensions

Similar to list comprehensions, dictionary comprehensions construct dictionaries concisely:

```python
base_prices = {"laptop": 1000, "mouse": 25, "monitor": 200}

# Add 8% sales tax to all prices:
taxed_prices = {item: round(price * 1.08, 2) for item, price in base_prices.items()}
# {'laptop': 1080.0, 'mouse': 27.0, 'monitor': 216.0}
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_07_Dictionaries_And_Sets.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Testing/Level_1_Beginner/Lesson_07_Dictionaries_And_Sets.py):

```python
# User Profile Database Management
users_db = {
    "USR-101": {"name": "Elena Rostova", "role": "Security Admin", "active": True},
    "USR-102": {"name": "Marcus Vance", "role": "DevOps Engineer", "active": False},
    "USR-103": {"name": "Sarah Connor", "role": "Lead Architect", "active": True},
}

active_admin_count = 0

print("--- Active User Directory ---")
for uid, profile in users_db.items():
    if profile["active"]:
        print(f"[{uid}] {profile['name']} - {profile['role']}")
        if "Admin" in profile["role"]:
            active_admin_count += 1

print(f"Total Active Security Admins: {active_admin_count}")
```

---

## 📝 Quick Exercise: E-Commerce Cart & Category Analytics Tracker

### 🏢 Real-Life Scenario
You are developing the shopping cart analytics module for an online computer hardware store. When a customer completes checkout, the system receives a raw list of scanned item slugs (with possible duplicate entries). The program must calculate item quantities, lookup prices from a catalog dictionary to generate an itemized bill, determine unique items purchased using sets, and cross-reference department category sets to identify promotional bundle eligibility.

### 📋 Requirements
1. Declare the baseline product and department collections:
   - `catalog`:
     ```python
     catalog = {
         "laptop": 999.99,
         "mouse": 29.50,
         "keyboard": 79.00,
         "monitor": 249.99,
         "usb_hub": 19.95
     }
     ```
   - `scanned_cart`:
     ```python
     scanned_cart = ["laptop", "mouse", "keyboard", "mouse", "usb_hub", "mouse", "monitor"]
     ```
   - Category and promo sets:
     - `peripherals = {"mouse", "keyboard", "monitor", "usb_hub"}`
     - `promo_eligible = {"mouse", "usb_hub", "keyboard"}`
2. Frequency count:
   - Use a `for` loop and `.get()` to populate an `item_counts` dictionary counting the quantity of each scanned item.
3. Billing & Totals:
   - Compute line totals for each unique item (`catalog[item] * count`), accumulate `grand_total`, and calculate total item units purchased.
4. Set Analytics:
   - Convert `scanned_cart` to a set `unique_purchased`.
   - Calculate purchased peripherals: `unique_purchased & peripherals`
   - Calculate promotional discount items: `unique_purchased & promo_eligible`
   - Calculate non-promotional standard items: `unique_purchased - promo_eligible`
5. Output the itemized checkout invoice and category analysis report.

> [!IMPORTANT]
> **Strict Constraint**: Use **only** concepts covered in Lessons 1 through 7 (variables, primitives, `input()`, numbers, strings, conditionals, loops, lists, tuples, dictionaries, dict methods, sets, set operators, f-strings, and `print()`). Do **not** use functions (`def`), files, or classes.

### 🎯 Expected Output
```text
==================================================
           APEX HARDWARE CHECKOUT AUDIT           
==================================================
ITEMIZED RECEIPT:
- Laptop            : 1 x $999.99 = $  999.99
- Mouse             : 3 x $ 29.50 = $   88.50
- Keyboard          : 1 x $ 79.00 = $   79.00
- Usb_hub           : 1 x $ 19.95 = $   19.95
- Monitor           : 1 x $249.99 = $  249.99
--------------------------------------------------
Total Units Scanned:  7 items
GRAND TOTAL INVOICE:  $1,437.43
--------------------------------------------------
CATEGORY & PROMO ANALYSIS:
Unique Products:      5 types
Peripherals Bought:   {'usb_hub', 'mouse', 'monitor', 'keyboard'}
Promo Discount Items: {'usb_hub', 'mouse', 'keyboard'}
Standard Price Items: {'laptop', 'monitor'}
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Product catalog, cart stream, and department sets
catalog = {
    "laptop": 999.99,
    "mouse": 29.50,
    "keyboard": 79.00,
    "monitor": 249.99,
    "usb_hub": 19.95
}

scanned_cart = ["laptop", "mouse", "keyboard", "mouse", "usb_hub", "mouse", "monitor"]

peripherals = {"mouse", "keyboard", "monitor", "usb_hub"}
promo_eligible = {"mouse", "usb_hub", "keyboard"}

# 2. Count item frequencies using dictionary .get()
item_counts = {}
for item in scanned_cart:
    item_counts[item] = item_counts.get(item, 0) + 1

# 3. Calculate invoice totals and display itemized lines
grand_total = 0.0
total_units = len(scanned_cart)

print("==================================================")
print("           APEX HARDWARE CHECKOUT AUDIT           ")
print("==================================================")
print("ITEMIZED RECEIPT:")

for item, count in item_counts.items():
    unit_price = catalog.get(item, 0.0)
    line_total = unit_price * count
    grand_total += line_total
    print(f"- {item.capitalize():<18}: {count} x ${unit_price:>6.2f} = ${line_total:>8.2f}")

print("--------------------------------------------------")
print(f"Total Units Scanned:  {total_units} items")
print(f"GRAND TOTAL INVOICE:  ${grand_total:,.2f}")
print("--------------------------------------------------")

# 4. Set operations for category and promo analysis
unique_purchased = set(scanned_cart)
purchased_peripherals = unique_purchased & peripherals
promotional_items = unique_purchased & promo_eligible
standard_items = unique_purchased - promo_eligible

print("CATEGORY & PROMO ANALYSIS:")
print(f"Unique Products:      {len(unique_purchased)} types")
print(f"Peripherals Bought:   {purchased_peripherals}")
print(f"Promo Discount Items: {promotional_items}")
print(f"Standard Price Items: {standard_items}")
print("==================================================")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What happens when you execute `data = {}; print(data["key"])`?**
   - A) Returns `None`
   - B) Returns `0`
   - C) Raises a `KeyError`
   - D) Adds `"key"` to the dictionary

2. **Why can a Python `tuple` be used as a dictionary key, but a `list` cannot?**
   - A) Tuples are faster.
   - B) Tuples are immutable and hashable, whereas lists are mutable and unhashable.
   - C) Tuples have fixed lengths.
   - D) Lists can only store numbers.

3. **Given `s1 = {1, 2, 3}` and `s2 = {2, 3, 4}`, what is the result of `s1 - s2`?**
   - A) `{1, 4}`
   - B) `{1}`
   - C) `{2, 3}`
   - D) `{4}`

<details>
<summary><b>View Answers</b></summary>
1: C (Direct square bracket access for a non-existent key throws a KeyError; use .get() for safe retrieval)<br>
2: B (Dictionary keys must be hashable, which requires immutability)<br>
3: B (Set difference s1 - s2 returns elements in s1 that do not exist in s2)
</details>
