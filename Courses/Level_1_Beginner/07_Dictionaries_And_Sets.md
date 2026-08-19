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
unique_emails.remove("carol@co.com")    # Raises KeyError if missing
unique_emails.discard("missing@co.com") # Safe: does not raise error if absent
```

---

## 5. Mathematical Set Algebra Operations

Sets excel at comparing groups and calculating overlapping permissions, shared assets, or differential security access:

```python
dev_team = {"Alice", "Bob", "Charlie", "David"}
ops_team = {"Charlie", "David", "Eve", "Frank"}

# 1. Union (|): All members across both teams
all_engineers = dev_team | ops_team
# {'Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'}

# 2. Intersection (&): Members in BOTH teams (DevOps engineers)
devops_members = dev_team & ops_team
# {'Charlie', 'David'}

# 3. Difference (-): Members in dev_team who are NOT in ops_team
pure_devs = dev_team - ops_team
# {'Alice', 'Bob'}

# 4. Symmetric Difference (^): Members in either dev OR ops, but NOT in both
specialized_only = dev_team ^ ops_team
# {'Alice', 'Bob', 'Eve', 'Frank'}
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
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Inventory Database & Vendor Sets (Lessons 1-7)
inventory_db = {
    "SKU-01": {"name": "4K Gaming Monitor", "category": "Electronics", "stock": 14, "cost": 349.99, "reorder_at": 10},
    "SKU-02": {"name": "Mechanical Keyboard", "category": "Accessories", "stock": 4, "cost": 89.50, "reorder_at": 15},
    "SKU-03": {"name": "Ergonomic Desk Chair", "category": "Furniture", "stock": 22, "cost": 210.00, "reorder_at": 5},
    "SKU-04": {"name": "USB-C Docking Station", "category": "Accessories", "stock": 0, "cost": 65.00, "reorder_at": 8},
    "SKU-05": {"name": "Standing Desk Frame", "category": "Furniture", "stock": 2, "cost": 299.00, "reorder_at": 6},
}

vendor_skus = {"SKU-01", "SKU-02", "SKU-03", "SKU-04", "SKU-05", "SKU-06", "SKU-07"}
internal_skus = set(inventory_db.keys())

# 2. Set Difference (Lesson 7)
new_vendor_products = vendor_skus - internal_skus

# 3. Analytics & Aggregations (Lessons 6 & 7)
total_warehouse_value = sum(item["stock"] * item["cost"] for item in inventory_db.values())
categories = sorted({item["category"] for item in inventory_db.values()})

# 4. Formatted Report Display (Lessons 1 & 7)
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
```

**Explanation of the Solution:**
- `inventory_db` maps SKU strings to nested dictionaries holding product properties.
- `vendor_skus - internal_skus` performs a set difference to isolate uncarried catalog items.
- A dictionary value comprehension calculates the aggregate financial value of stored physical inventory.
</details>
