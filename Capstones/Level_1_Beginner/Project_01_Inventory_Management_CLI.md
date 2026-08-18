# Capstone Project 1.1: Retail Inventory Management CLI

## 📌 Project Overview
Build an interactive command-line **Retail Inventory & Stock Management System** for a store. The application allows store managers to manage products, adjust inventory levels, search items with flexible filters, calculate inventory valuations, and generate low-stock alert reports with automated file persistence.

---

## 🎯 Learning Objectives
By completing this project, you will demonstrate mastery of:
- **Collections**: Managing complex entity catalogs with dictionaries and lists.
- **Control Flow**: Implementing an infinite menu loop with robust input validation.
- **File I/O**: Persisting inventory records to and from disk (`JSON` or `CSV`).
- **Defensive Error Handling**: Catching `ValueError`, `KeyError`, and `FileNotFoundError`.
- **OOP Basics**: Encapsulating data and behavior inside `Product` and `Inventory` classes.

---

## 🏗️ System Architecture

```text
+-----------------------------------------------------------+
|                     Inventory CLI                         |
+-----------------------------------------------------------+
                              |
               +--------------+--------------+
               |                             |
     +-------------------+         +-------------------+
     |   Product Model   |         | Inventory Manager |
     +-------------------+         +-------------------+
     | - sku: str        |         | - items: dict     |
     | - name: str       |         | - filepath: str   |
     | - price: float    |         | + add_product()   |
     | - quantity: int   |         | + update_stock()  |
     | - category: str   |         | + search()        |
     | + get_value()     |         | + save_to_file()  |
     +-------------------+         | + load_from_file()|
                                   +-------------------+
```

---

## 📋 Functional Requirements

### 1. Product Entity
Each product in the inventory must have:
- `sku` (str, Unique Identifier, e.g., `"SKU-1001"`)
- `name` (str)
- `category` (str, e.g., `"Electronics"`, `"Groceries"`, `"Clothing"`)
- `price` (float, must be positive)
- `quantity` (int, must be non-negative)
- `min_threshold` (int, threshold for low stock alert, default `5`)

### 2. Core Operations (CLI Menu)
Your system must provide an interactive console loop with the following options:
1. **List All Products**: Display a cleanly formatted ASCII table of all products with SKU, Name, Category, Price, Quantity, and Total Stock Value.
2. **Add New Product**: Prompt user for details. Prevent duplicate SKUs and reject negative prices/quantities.
3. **Update Stock Quantity**: Allow increasing (restocking) or decreasing (sales) of existing SKUs.
4. **Search & Filter**: Search products by substring in name or filter by category.
5. **Low Stock Alert**: List all items where `quantity <= min_threshold`.
6. **Financial Valuation**: Calculate total inventory item count and total asset value (`sum(price * quantity)`).
7. **Save & Exit**: Write all data to `inventory.json` or `inventory.csv` before exiting.

---

## 📐 Phased Implementation Guide

### Phase 1: Product Representation & Validation
Create the `Product` class with a constructor, representation method, and helper calculations:
```python
class Product:
    def __init__(self, sku: str, name: str, category: str, price: float, quantity: int, min_threshold: int = 5):
        self.sku = sku
        self.name = name
        self.category = category
        self.price = float(price)
        self.quantity = int(quantity)
        self.min_threshold = int(min_threshold)

    def get_total_value(self) -> float:
        return self.price * self.quantity

    def to_dict(self) -> dict:
        return {
            "sku": self.sku,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "min_threshold": self.min_threshold
        }
```

### Phase 2: Inventory Manager Class
Create the `InventoryManager` class that stores products in a dictionary keyed by `sku`:
```python
class InventoryManager:
    def __init__(self, data_file: str = "inventory.json"):
        self.data_file = data_file
        self.products = {}  # Dict[str, Product]
        self.load_from_file()

    def add_product(self, product: Product) -> bool:
        if product.sku in self.products:
            raise ValueError(f"SKU '{product.sku}' already exists.")
        self.products[product.sku] = product
        return True

    def adjust_stock(self, sku: str, amount: int) -> int:
        if sku not in self.products:
            raise KeyError(f"Product '{sku}' not found.")
        new_qty = self.products[sku].quantity + amount
        if new_qty < 0:
            raise ValueError("Insufficient stock for deduction.")
        self.products[sku].quantity = new_qty
        return new_qty
```

### Phase 3: File Persistence
Implement JSON serialization and deserialization with graceful handling when files do not yet exist.

### Phase 4: Interactive Menu & Defensive CLI
Build a loop with formatted text, input validation, and user confirmation prompts.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Duplicate SKU** | Add product with an already existing SKU | Prints error message, returns to menu without overwriting |
| **Negative Input** | Enter price `-15.99` or quantity `-5` | Rejects input with `ValueError`, prompts user to re-enter |
| **Missing File** | Run app when `inventory.json` does not exist | Initializes empty catalog gracefully without crashing |
| **Overselling** | Deduct 20 units when only 5 are in stock | Raises error, keeps stock unchanged at 5 |
| **Case Insensitive Search**| Search for `"laptop"` when product is `"Gaming Laptop"` | Successfully matches and returns the item |

---

## 🚀 Bonus Challenges
- **CSV Export**: Add an option to export inventory reports to a timestamped CSV file (`inventory_report_YYYYMMDD.csv`).
- **Discount Promotions**: Add a feature to apply a percentage discount across an entire category.
