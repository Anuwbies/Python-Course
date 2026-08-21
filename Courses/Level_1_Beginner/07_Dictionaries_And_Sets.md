# Lesson 7: Mapping & Unique Collections: Dictionaries & Sets

When working with complex datasets, looking up items by numeric index is often insufficient. We need to look up records by meaningful keys (such as user IDs, email addresses, or product SKUs) and maintain deduplicated collections. In this lesson, you will master Python's two hash-table-backed data structures: **Dictionaries** (`dict`) and **Sets** (`set`).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Create and manage associative key-value **Dictionaries** (`dict`).
2. Perform safe key lookups using `.get(key, default)` and prevent `KeyError` crashes.
3. Iterate over dictionaries using `.keys()`, `.values()`, and `.items()`.
4. Construct **Dictionary Comprehensions** for rapid data mapping and filtering.
5. Create unique, deduplicated **Sets** (`set`) and perform set mutations.
6. Execute mathematical set algebra operations: Union (`|`), Intersection (`&`), Difference (`-`), and Symmetric Difference (`^`).

---

## 1. Dictionaries: Key-Value Mappings

A Python dictionary is a mutable, ordered (in Python 3.7+) mapping of unique, hashable keys to arbitrary values. Key lookups operate in near-instantaneous $O(1)$ constant time.

```python
# Initializing a dictionary:
server_node = {
    "hostname": "prod-api-01",
    "ip_address": "192.168.1.105",
    "cpu_cores": 32,
    "memory_gb": 128.0,
    "is_active": True
}

# 1. Accessing and Updating Values:
print(server_node["hostname"])    # "prod-api-01"
server_node["memory_gb"] = 256.0  # Update existing key
server_node["region"] = "us-east" # Add new key-value pair

# 2. Safe Lookups with .get():
# Direct lookup server_node["rack_id"] -> Raises KeyError!
rack = server_node.get("rack_id", "RACK-UNKNOWN") # Returns fallback default value
print(f"Rack Location: {rack}")

# 3. Removing Items:
region = server_node.pop("region", None) # Removes and returns key
```

---

## 2. Iterating Over Dictionaries

Python provides three essential views for dictionary iteration:

```python
cluster_metrics = {"web_app": 45, "database": 88, "cache": 12, "queue": 65}

# 1. Iterate over keys (default):
for service in cluster_metrics.keys():
    print(f"Service: {service}")

# 2. Iterate over values:
for cpu_pct in cluster_metrics.values():
    print(f"CPU Load: {cpu_pct}%")

# 3. Iterate over (key, value) pairs simultaneously:
for service, cpu_pct in cluster_metrics.items():
    print(f"Node [{service:<10}] -> CPU: {cpu_pct}%")
```

---

## 3. Dictionary Comprehensions

Transform and filter key-value pairs cleanly in one readable line:

$$\text{new\_dict} = \{\textbf{key\_expr}: \textbf{val\_expr} \textbf{ for } \text{k}, \text{v} \textbf{ in } \text{source.items()} \textbf{ if } \text{condition}\}$$

```python
price_catalog_usd = {"laptop": 1200.0, "mouse": 25.0, "keyboard": 75.0, "monitor": 300.0}

# 1. Applying a 10% holiday discount to all items:
discounted_catalog = {item: price * 0.90 for item, price in price_catalog_usd.items()}

# 2. Filtering only high-ticket items (price > $100):
premium_items = {item: price for item, price in price_catalog_usd.items() if price > 100.0}
```

---

## 4. Sets: Unique, Deduplicated Collections

A `set` is an unordered collection of unique, immutable elements. Sets do not allow duplicate items and provide $O(1)$ membership checks (`item in set`).

```python
# 1. Deduplicating a list of customer email signups:
raw_signups = ["alice@co.com", "bob@co.com", "alice@co.com", "carol@co.com", "bob@co.com"]
unique_emails = set(raw_signups)
print(unique_emails) # {'alice@co.com', 'bob@co.com', 'carol@co.com'}

# 2. Set mutations:
unique_emails.add("dave@co.com")
---

## 6. CPython Hash Table Internals & Key Hashability

Under the hood, both `dict` and `set` are implemented as **hash tables**. 

```
Key String: "alice@co.com" ──► hash("alice@co.com") ──► 7349182348123 ──► Bucket Index: 3
[ Bucket 3 ] ──► Stores Pointer to {"alice@co.com": "User Object"}
```

### 🔑 Why Must Keys Be Hashable (Immutable)?
A dictionary key must never change its hash value during its lifetime. 
- **Hashable Types (Valid Keys)**: `str`, `int`, `float`, `tuple`, `frozenset`, `bool`.
- **Unhashable Types (Invalid Keys)**: `list`, `dict`, `set` (modifying their contents would change their hash and break the lookup table!).

```python
# ❌ TypeError: unhashable type: 'list'
# bad_dict = {[1, 2]: "coordinates"}

# ✅ CORRECT: Use an immutable tuple as key:
good_dict = {(1, 2): "coordinates"}
```

### ⚡ Python 3.7+ Compact Dict Layout
Since Python 3.7, dictionaries maintain **key insertion order** while consuming up to 25% less memory by splitting storage into a dense entries array and a sparse indices table.

---

## 7. Modern Dictionary Operators (`|` and `|=`) & `collections` Helpers

### 1. Dictionary Merge Operators (Python 3.9+)
Merge two dictionaries into a new one using `|`, or update in place with `|=`:

```python
default_config = {"host": "localhost", "port": 8000, "debug": False}
custom_config  = {"port": 9000, "debug": True, "ssl": True}

# Merge creates a new dict with custom values overriding defaults:
merged_config = default_config | custom_config
print(merged_config)
# {'host': 'localhost', 'port': 9000, 'debug': True, 'ssl': True}
```

### 2. `collections.defaultdict` and `collections.Counter`
```python
from collections import defaultdict, Counter

# defaultdict eliminates KeyError and .get(k, 0) boilerplate:
tally = defaultdict(int)
for word in ["apple", "banana", "apple"]:
    tally[word] += 1

# Counter counts frequency automatically:
counts = Counter(["apple", "banana", "apple", "orange", "apple"])
print(counts.most_common(1)) # [('apple', 3)]
```

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Role-Based Access Control (RBAC) & Security Audit Engine**, utilizing all dictionary and set concepts taught in this lesson:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Enterprise RBAC Authorization & Security Auditor
# =====================================================================

print("=" * 70)
print(f"{'🔐 ENTERPRISE IDENTITY & ACCESS MANAGEMENT (IAM) GATEWAY':^70}")
print("=" * 70)

# 1. Role Permission Matrix modeled with Sets (Lesson 7)
ROLE_PERMISSIONS = {
    "admin": {"read", "write", "delete", "deploy", "audit", "billing"},
    "developer": {"read", "write", "deploy"},
    "auditor": {"read", "audit", "billing"},
    "support": {"read", "write"}
}

# 2. User Directory modeled as Nested Dictionaries (Lesson 7)
user_directory = {
    "USR-101": {"name": "Elena Rostova", "role": "admin", "department": "Security", "active": True},
    "USR-102": {"name": "Marcus Vance", "role": "developer", "department": "Engineering", "active": True},
    "USR-103": {"name": "Sarah Connor", "role": "developer", "department": "Engineering", "active": False},
    "USR-104": {"name": "David Kim", "role": "auditor", "department": "Finance", "active": True},
    "USR-105": {"name": "Chloe Price", "role": "support", "department": "Customer Ops", "active": True},
}

# 3. Security Audit: Extract all active users by Department (Dict & Set Comprehensions)
active_users = {uid: u for uid, u in user_directory.items() if u["active"]}
active_departments = {u["department"] for u in active_users.values()}

# 4. Compliance Auditing: Find all permissions granted to active Engineering staff
eng_roles = {u["role"] for u in active_users.values() if u["department"] == "Engineering"}
eng_permissions = set()
for role in eng_roles:
    eng_permissions |= ROLE_PERMISSIONS.get(role, set())

# High-Risk Privileges that require dual authorization
CRITICAL_PRIVILEGES = {"delete", "billing", "deploy"}
eng_critical_exposure = eng_permissions & CRITICAL_PRIVILEGES

# 5. Access Authorization Function Simulation
def verify_access(user_id: str, required_action: str) -> tuple[bool, str]:
    user = user_directory.get(user_id)
    if not user:
        return False, "User ID not registered in IAM directory"
    if not user["active"]:
        return False, "Account suspended: Security lockout"
    
    user_role = user.get("role", "")
    granted_perms = ROLE_PERMISSIONS.get(user_role, set())
    
    if required_action in granted_perms:
        return True, f"Action '{required_action}' authorized for role '{user_role}'"
    return False, f"Permission Denied: '{user_role}' lacks '{required_action}' capability"

# 6. Audit Report Display (Lessons 1 & 7)
print(f"{'IAM Metric':<35} | {'Value':>30}")
print("-" * 70)
print(f"{'Total Registered Accounts':<35} | {len(user_directory):>30}")
print(f"{'Active User Accounts':<35} | {len(active_users):>30}")
print(f"{'Active Operational Departments':<35} | {len(active_departments):>30}")
print(f"{'Engineering Critical Permissions':<35} | {str(eng_critical_exposure):>30}")
print("=" * 70)

# Simulating runtime authorization checks
print(f"{'RUNTIME AUTHORIZATION AUDIT LOGS':^70}")
print("-" * 70)

test_scenarios = [
    ("USR-101", "delete"),
    ("USR-102", "deploy"),
    ("USR-102", "billing"),
    ("USR-103", "read"),
    ("USR-999", "read"),
]

for uid, action in test_scenarios:
    allowed, reason = verify_access(uid, action)
    status_tag = "✅ GRANTED" if allowed else "❌ REJECTED"
    print(f"[{status_tag}] User {uid} -> Action '{action}': {reason}")

print("=" * 70)
```

### 🔍 Code Explanation:
- **Set-Backed Roles**: `ROLE_PERMISSIONS` maps role names to sets of permissions, allowing fast membership checks (`required_action in granted_perms`) and set operations.
- **Nested Dictionaries**: `user_directory` stores structured metadata indexed by unique employee ID keys (`USR-101`).
- **Comprehensions**: `{uid: u for uid, u in user_directory.items() if u["active"]}` filters only active personnel into a dedicated audit dictionary.
- **Set Algebra**: `eng_permissions & CRITICAL_PRIVILEGES` calculates the intersection between engineering permissions and sensitive actions to identify high-risk access exposure.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master dictionaries, safe lookups, dictionary comprehensions, sets, set algebra, and compact hash table structures:

---

### 🟢 Tier 1: Dictionary CRUD & Safe Access (Exercises 1–3)

#### 🔹 Exercise 1: Contact Directory Manager
* **Goal**: Create `contacts = {"alice": "555-0100", "bob": "555-0101"}`.
* **Operations**: Add `"charlie": "555-0102"`, update `"alice"`'s phone, and query `"david"` safely using `.get("david", "Not Found")`.

#### 🔹 Exercise 2: Word Frequency Counter (Classic Mapping)
* **Goal**: Given word list `words = ["apple", "banana", "apple", "orange", "banana", "apple"]`.
* **Requirement**: Use a `for` loop with `tally[w] = tally.get(w, 0) + 1` to generate a frequency dictionary.

#### 🔹 Exercise 3: Key/Value View Iteration
* **Goal**: Given `rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 155.0}`.
* **Requirement**: Use a `for currency, rate in rates.items():` loop to print each formatted rate.

---

### 🟡 Tier 2: Comprehensions & Set Operations (Exercises 4–6)

#### 🔹 Exercise 4: Dictionary Price Discount Comprehension
* **Goal**: Given `catalog = {"laptop": 1200, "mouse": 25, "keyboard": 75, "monitor": 300}`.
* **Requirement**: Use a dict comprehension to apply a 15% discount only to items with price $> \$50$: `{k: round(v*0.85, 2) for k, v in catalog.items() if v > 50}`.

#### 🔹 Exercise 5: Set Algebra Permission Auditor
* **Goal**: Given `user_perms = {"read", "write", "upload"}` and `admin_perms = {"read", "write", "delete", "grant_access"}`.
* **Calculation**: Find (1) shared permissions (`&`), (2) missing admin permissions (`admin_perms - user_perms`), (3) all unique combined permissions (`|`).

#### 🔹 Exercise 6: Inverted Dictionary (Value-to-Key Mapping)
* **Goal**: Given `user_to_id = {"alice": 101, "bob": 102, "charlie": 103}`.
* **Requirement**: Use a dictionary comprehension to swap keys and values: `{v: k for k, v in user_to_id.items()}`.

---

### 🟠 Tier 3: Nested Mappings & Modern Operators (Exercises 7–9)

#### 🔹 Exercise 7: Nested Employee Roster Deep Query
* **Goal**: Given `company = {"eng": {"lead": "Alice", "staff": 8}, "sales": {"lead": "Bob", "staff": 14}}`.
* **Requirement**: Add `"finance": {"lead": "Carol", "staff": 4}`, and calculate the total company staff count using a generator expression inside `sum()`.

#### 🔹 Exercise 8: Config Merge with `|` Operator (Python 3.9+)
* **Goal**: Given `default_env = {"debug": False, "timeout": 30, "threads": 4}` and `override_env = {"debug": True, "threads": 8}`.
* **Requirement**: Merge using `merged = default_env | override_env`. Print final configuration.

#### 🔹 Exercise 9: Frequency Top-K Analysis with `collections.Counter`
* **Goal**: Given a long text passage, tokenize into words and use `Counter(words).most_common(3)` to find the top 3 most frequent words.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Warehouse Inventory Valuation & Restock Dispatcher
* **Goal**: Nested dictionary inventory database, set difference comparison against vendor master catalog, reorder threshold alerts, and valuation metrics.

---

## 📝 Quick Exercise: E-Commerce Inventory Stock & Category Reorder Hub

### 🏢 Real-Life Scenario
You are developing the inventory control and automated warehouse restock engine for an online retailer. The warehouse stores products across various categories with current stock counts, reorder thresholds, and unit costs. The program must allow the manager to query items, calculate total inventory valuation, identify out-of-stock items, and calculate missing items between vendor catalog and internal warehouse inventory using set operations.

### 📋 Requirements
1. Initialize the internal warehouse database:
   ```python
   inventory_db = {
       "SKU-01": {"name": "4K Gaming Monitor", "category": "Electronics", "stock": 14, "cost": 349.99, "reorder_at": 10},
       "SKU-02": {"name": "Mechanical Keyboard", "category": "Accessories", "stock": 4, "cost": 89.50, "reorder_at": 15},
       "SKU-03": {"name": "Ergonomic Desk Chair", "category": "Furniture", "stock": 22, "cost": 210.00, "reorder_at": 5},
       "SKU-04": {"name": "USB-C Docking Station", "category": "Accessories", "stock": 0, "cost": 65.00, "reorder_at": 8},
       "SKU-05": {"name": "Standing Desk Frame", "category": "Furniture", "stock": 2, "cost": 299.00, "reorder_at": 6},
   }
   ```
2. Vendor Product Catalog (Set Comparison):
   - Vendor catalog set: `vendor_skus = {"SKU-01", "SKU-02", "SKU-03", "SKU-04", "SKU-05", "SKU-06", "SKU-07"}`
   - Internal warehouse set: `internal_skus = set(inventory_db.keys())`
   - Compute `new_vendor_products = vendor_skus - internal_skus` (products offered by vendor that we do not carry).
3. Analytics Calculations:
   - Compute `total_warehouse_value = sum(item["stock"] * item["cost"] for item in inventory_db.values())`.
   - Identify items needing restock: `reorder_list = [item["name"] for item in inventory_db.values() if item["stock"] <= item["reorder_at"]]`.
   - Identify distinct product categories using a **Set Comprehension**: `categories = {item["category"] for item in inventory_db.values()}`.
4. Output the complete inventory evaluation and reorder report using formatted f-strings.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine concepts from **Lessons 1 through 7** (variables, types, arithmetic, compound conditionals, while/for loops, lists, tuples, dict lookups `.get()`, dict comprehensions, sets, and set difference `-`).

### 🎯 Expected Output
```text
==================================================
        WAREHOUSE INVENTORY & REORDER REPORT      
==================================================
Total Unique SKUs:     5 items
Distinct Categories:   3 (Accessories, Electronics, Furniture)
Total Valuation:       $10,286.86
--------------------------------------------------
ITEMS REQUIRING IMMEDIATE RESTOCK (<= Reorder Threshold):
  - Mechanical Keyboard (Stock: 4 | Min: 15)
  - USB-C Docking Station (Stock: 0 | Min: 8) [OUT OF STOCK 🚨]
  - Standing Desk Frame (Stock: 2 | Min: 6)
--------------------------------------------------
NEW VENDOR PRODUCTS AVAILABLE TO CARRY (Set Difference):
  - SKU-06
  - SKU-07
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Inventory & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Warehouse Inventory & Reorder Report
# =====================================================================
inventory_db = {
    "SKU-01": {"name": "4K Gaming Monitor", "category": "Electronics", "stock": 14, "cost": 349.99, "reorder_at": 10},
    "SKU-02": {"name": "Mechanical Keyboard", "category": "Accessories", "stock": 4, "cost": 89.50, "reorder_at": 15},
    "SKU-03": {"name": "Ergonomic Desk Chair", "category": "Furniture", "stock": 22, "cost": 210.00, "reorder_at": 5},
    "SKU-04": {"name": "USB-C Docking Station", "category": "Accessories", "stock": 0, "cost": 65.00, "reorder_at": 8},
    "SKU-05": {"name": "Standing Desk Frame", "category": "Furniture", "stock": 2, "cost": 299.00, "reorder_at": 6},
}

vendor_skus = {"SKU-01", "SKU-02", "SKU-03", "SKU-04", "SKU-05", "SKU-06", "SKU-07"}
internal_skus = set(inventory_db.keys())

new_vendor_products = vendor_skus - internal_skus
total_warehouse_value = sum(item["stock"] * item["cost"] for item in inventory_db.values())
categories = sorted({item["category"] for item in inventory_db.values()})

print("==================================================")
print("        WAREHOUSE INVENTORY & REORDER REPORT      ")
print("==================================================")
print(f"Total Unique SKUs:     {len(inventory_db)} items")
print(f"Distinct Categories:   {len(categories)} ({', '.join(categories)})")
print(f"Total Valuation:       ${total_warehouse_value:,.2f}")
print("--------------------------------------------------")
print("ITEMS REQUIRING IMMEDIATE RESTOCK (<= Reorder Threshold):")

for sku, data in inventory_db.items():
    if data["stock"] <= data["reorder_at"]:
        alert = " [OUT OF STOCK 🚨]" if data["stock"] == 0 else ""
        print(f"  - {data['name']} (Stock: {data['stock']} | Min: {data['reorder_at']}){alert}")

print("--------------------------------------------------")
print("NEW VENDOR PRODUCTS AVAILABLE TO CARRY (Set Difference):")
for sku in sorted(new_vendor_products):
    print(f"  - {sku}")

print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
contacts = {"alice": "555-0100", "bob": "555-0101"}
contacts["charlie"] = "555-0102"
contacts["alice"] = "555-9999"
print("David:", contacts.get("david", "Not Found"))

# Ex 2:
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
tally = {}
for w in words: tally[w] = tally.get(w, 0) + 1
print(f"Tally: {tally}")

# Ex 3:
rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 155.0}
for curr, r in rates.items():
    print(f"1 USD = {r} {curr}")

# Ex 4:
catalog = {"laptop": 1200, "mouse": 25, "keyboard": 75, "monitor": 300}
disc = {k: round(v * 0.85, 2) for k, v in catalog.items() if v > 50}
print(f"Discounted: {disc}")

# Ex 5:
user_perms = {"read", "write", "upload"}
admin_perms = {"read", "write", "delete", "grant_access"}
print(f"Shared: {user_perms & admin_perms}")
print(f"Missing Admin: {admin_perms - user_perms}")
print(f"All Unique: {user_perms | admin_perms}")

# Ex 6:
user_to_id = {"alice": 101, "bob": 102, "charlie": 103}
id_to_user = {v: k for k, v in user_to_id.items()}
print(f"Inverted: {id_to_user}")

# Ex 7:
company = {"eng": {"lead": "Alice", "staff": 8}, "sales": {"lead": "Bob", "staff": 14}}
company["finance"] = {"lead": "Carol", "staff": 4}
total_staff = sum(dept["staff"] for dept in company.values())
print(f"Total Staff: {total_staff}")

# Ex 8:
default_env = {"debug": False, "timeout": 30, "threads": 4}
override_env = {"debug": True, "threads": 8}
merged = default_env | override_env
print(f"Merged Config: {merged}")

# Ex 9:
from collections import Counter
txt = "python is fast and python is readable and python is powerful"
top3 = Counter(txt.split()).most_common(3)
print(f"Top 3 Words: {top3}")
```
</details>

