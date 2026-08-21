# Lesson 10: Object-Oriented Programming (OOP) Fundamentals

Throughout the previous lessons, we used procedural functions and individual dictionaries/lists. However, as software systems grow complex, modeling business entities by grouping related data (state) and functions (behavior) together becomes essential. In this milestone lesson, you will master Python's **Object-Oriented Programming (OOP)** foundations: Classes, Instances, Constructors, Methods, and Attributes.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the core principles of Object-Oriented Programming and Domain Modeling.
2. Define custom classes using the `class` keyword.
3. Initialize object state using the `__init__()` constructor and understand the `self` reference.
4. Distinguish between **Instance Attributes** (unique per object) and **Class Attributes** (shared across all instances).
5. Implement Instance Methods that inspect and modify object state.
6. Provide readable string representations of objects using `__str__()` and `__repr__()`.

---

## 1. Classes vs. Instances

- **Class**: The blueprint or template that defines properties and behaviors (e.g. `BankAccount`).
- **Instance (Object)**: An individual, concrete realization created in memory from that blueprint (e.g. `alice_account = BankAccount("Alice", 1000.0)`).

```python
class ServerNode:
    """Blueprint representing a cloud computing node."""
    
    # Class Attribute (Shared by ALL ServerNode instances):
    CLOUD_REGION = "us-east-1"
    
    # Constructor: Runs automatically when a new object is instantiated
    def __init__(self, hostname: str, ip_address: str, ram_gb: float):
        # Instance Attributes (Unique to each specific server):
        self.hostname = hostname
        self.ip_address = ip_address
        self.ram_gb = ram_gb
        self.is_active = True
        self.active_connections = 0

    # Instance Method:
    def connect_client(self) -> bool:
        """Increments active connections if the server is active."""
        if not self.is_active:
            print(f"❌ Connection rejected: {self.hostname} is offline.")
            return False
        self.active_connections += 1
        return True

    def shutdown(self) -> None:
        """Transitions server node to offline status."""
        self.is_active = False
        self.active_connections = 0
        print(f"🛑 Server {self.hostname} has been cleanly shut down.")
```

---

## 2. The `self` Parameter Explained

In Python, every instance method must receive `self` as its first parameter. 

When you write:
```python
node1 = ServerNode("node-01", "10.0.0.1", 32.0)
node1.connect_client()
```
Python automatically translates this invocation to:
```python
ServerNode.connect_client(node1) # 'self' references node1 in memory
```

---

## 3. Class Attributes vs. Instance Attributes

```python
class Employee:
    # Class Attribute: Shared across the company
    COMPANY_NAME = "Apex Technologies Inc."
    TOTAL_EMPLOYEES = 0 # Counter for all instances created

    def __init__(self, name: str, role: str):
        # Instance Attributes: Unique to this employee
        self.name = name
        self.role = role
        Employee.TOTAL_EMPLOYEES += 1

emp1 = Employee("Elena", "Lead Architect")
emp2 = Employee("Marcus", "DevOps Engineer")

print(emp1.COMPANY_NAME)        # "Apex Technologies Inc."
print(Employee.TOTAL_EMPLOYEES) # 2 (Updated by both instances)
```

---

---

## 5. Encapsulation & Access Conventions in Python

Unlike C++ or Java, Python does not have strict `private` keywords enforced by the compiler. Instead, it relies on naming conventions:

| Convention | Syntax | Meaning | Behavior |
| :--- | :--- | :--- | :--- |
| **Public** | `self.balance` | Part of public API | Directly accessible by all callers |
| **Protected** | `self._balance` | Internal implementation detail | Accessible, but signals: "Do not touch outside the class hierarchy" |
| **Private (Name Mangled)** | `self.__balance` | Strictly private to class | Python automatically mangles name to `_ClassName__balance` to prevent accidental override |

```python
class BankAccount:
    def __init__(self, owner: str, initial_balance: float):
        self.owner = owner          # Public
        self._account_type = "SAVINGS" # Protected convention
        self.__pin = "1234"         # Private (mangled to _BankAccount__pin)

account = BankAccount("Alice", 500.0)
print(account.owner)            # "Alice"
print(account._account_type)    # "SAVINGS" (Allowed, but discouraged)
# print(account.__pin)          # ❌ AttributeError: 'BankAccount' object has no attribute '__pin'
print(account._BankAccount__pin)# "1234" (Mangled name access)
```

---

## 6. Instance Methods vs. `@classmethod` vs. `@staticmethod`

```python
class ServerCluster:
    DEFAULT_REGION = "us-east-1"

    def __init__(self, cluster_name: str, node_count: int):
        self.cluster_name = cluster_name # Instance attribute
        self.node_count = node_count

    # 1. Instance Method: Receives 'self' (can read/modify instance and class state)
    def scale_up(self, extra_nodes: int) -> None:
        self.node_count += extra_nodes

    # 2. Class Method: Receives 'cls' (can read/modify class state or act as factory constructor)
    @classmethod
    def create_development_cluster(cls, cluster_name: str):
        return cls(f"DEV-{cluster_name}", node_count=2)

    # 3. Static Method: Receives no automatic self/cls reference (utility function tied to class scope)
    @staticmethod
    def is_valid_cluster_name(name: str) -> bool:
        return name.isalnum() and len(name) >= 3

# Using instance, class, and static methods:
dev_cluster = ServerCluster.create_development_cluster("Analytics")
dev_cluster.scale_up(4)
print(f"Cluster: {dev_cluster.cluster_name}, Nodes: {dev_cluster.node_count}")
print(f"Name valid: {ServerCluster.is_valid_cluster_name('Analytics01')}")
```

---

## 💻 Code Example & Reference

The following real-life program models a **Commercial Airline Passenger Flight & Seat Booking Management System**, using all OOP and procedural concepts taught across Level 1:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Commercial Airline Flight & Reservation System
# =====================================================================

class Passenger:
    """Represents a ticketed flight passenger."""
    
    def __init__(self, passport_no: str, full_name: str, is_frequent_flyer: bool = False):
        self.passport_no = passport_no
        self.full_name = full_name
        self.is_frequent_flyer = is_frequent_flyer
        self.checked_bags = 0

    def add_checked_bag(self) -> None:
        self.checked_bags += 1

    def __str__(self) -> str:
        status = "★ Gold Member" if self.is_frequent_flyer else "Standard Passenger"
        return f"{self.full_name} ({self.passport_no}) - {status} [{self.checked_bags} bags]"


class CommercialFlight:
    """Manages an airliner flight route, capacity, and passenger manifest."""
    
    AIRLINE_NAME = "Apex Continental Airways" # Class Attribute
    
    def __init__(self, flight_number: str, origin: str, destination: str, seat_capacity: int, ticket_price: float):
        self.flight_number = flight_number
        self.origin = origin.upper()
        self.destination = destination.upper()
        self.seat_capacity = seat_capacity
        self.ticket_price = ticket_price
        self.passengers: list[Passenger] = []

    @property
    def seats_available(self) -> int:
        return self.seat_capacity - len(self.passengers)

    def book_passenger(self, passenger: Passenger) -> tuple[bool, str]:
        """Attempts to assign a passenger to this flight."""
        if self.seats_available <= 0:
            return False, f"Flight {self.flight_number} is FULL. Booking rejected."
            
        # Check duplicate booking
        for existing in self.passengers:
            if existing.passport_no == passenger.passport_no:
                return False, f"Passenger {passenger.passport_no} is already booked on this flight."
                
        self.passengers.append(passenger)
        return True, f"Passenger {passenger.full_name} confirmed on flight {self.flight_number}."

    def calculate_gross_revenue(self) -> float:
        return len(self.passengers) * self.ticket_price

    def print_manifest(self) -> None:
        print("\n" + "=" * 65)
        print(f"{CommercialFlight.AIRLINE_NAME:^65}")
        print(f"{'OFFICIAL PASSENGER FLIGHT MANIFEST':^65}")
        print("=" * 65)
        print(f"{'Flight:':<20} {self.flight_number} ({self.origin} -> {self.destination})")
        print(f"{'Capacity:':<20} {len(self.passengers)} / {self.seat_capacity} seats booked")
        print(f"{'Ticket Fare:':<20} ${self.ticket_price:,.2f}")
        print(f"{'Gross Flight Revenue:':<20} ${self.calculate_gross_revenue():,.2f}")
        print("-" * 65)
        print("PASSENGER ROSTER:")
        if not self.passengers:
            print("  (No passengers booked)")
        else:
            for idx, p in enumerate(self.passengers, start=1):
                print(f"  {idx:02d}. {p}")
        print("=" * 65)


# Executing the flight booking system
flight = CommercialFlight("APX-842", "JFK", "LHR", seat_capacity=3, ticket_price=850.00)

p1 = Passenger("US-90182", "Elena Rostova", is_frequent_flyer=True)
p1.add_checked_bag()
p1.add_checked_bag()

p2 = Passenger("UK-34190", "Marcus Vance", is_frequent_flyer=False)
p3 = Passenger("CA-88123", "Sarah Connor", is_frequent_flyer=True)
p4 = Passenger("FR-55412", "David Kim", is_frequent_flyer=False) # Exceeds capacity

for p in (p1, p2, p3, p4):
    success, msg = flight.book_passenger(p)
    tag = "✅" if success else "❌"
    print(f"{tag} {msg}")

flight.print_manifest()
```

### 🔍 Code Explanation:
- **Entity Modeling**: `Passenger` and `CommercialFlight` encapsulate independent responsibilities.
- **Composition**: `CommercialFlight` contains a list of `Passenger` objects, demonstrating object relationships.
- **Class Attributes**: `AIRLINE_NAME` is shared globally by all flight instances.
- **State Validation**: `book_passenger` validates seat capacity limits and enforces passport uniqueness before mutating the internal passenger list.

---

## 📝 Quick Exercise: Hospital Pharmacy Prescription & Inventory Control Engine

### 🏢 Real-Life Scenario
You are developing the pharmacy dispensing and prescription validation system for a regional hospital network. The system models pharmaceutical medications (`Medication`) and patients (`Patient`), tracking available dosages, prescription dispensing, inventory depletion, and patient allergic reactions.

### 📋 Requirements
1. **Define the `Medication` Class**:
   - Constructor: `__init__(self, code: str, name: str, stock_units: int, unit_cost: float)`
   - Methods:
     - `dispense(self, units: int) -> bool`: If `units <= self.stock_units`, deduct `units` from stock and return `True`; otherwise return `False`.
     - `restock(self, units: int) -> None`: Adds `units` to `stock_units`.
     - `__str__(self)`: Returns `f"[{self.code}] {self.name} - Stock: {self.stock_units} units (${self.unit_cost:.2f}/unit)"`.
2. **Define the `Patient` Class**:
   - Constructor: `__init__(self, patient_id: str, name: str, allergies: list[str] = None)`
   - Instance attributes: `patient_id`, `name`, `allergies` (a `set` of allergy names converted to lowercase), and `prescriptions` (a list of active medication names).
   - Method:
     - `prescribe(self, med: Medication, units: int) -> tuple[bool, str]`:
       - Check if medication name (lowercase) is in `self.allergies`. If so, return `False, "ALLERGY ALERT: Patient is allergic to this medication!"`.
       - Attempt to dispense from `med.dispense(units)`. If stock is insufficient, return `False, "INVENTORY ERROR: Insufficient pharmacy stock"`.
       - If safe and in stock, add medication name to `self.prescriptions` and return `True, f"Successfully dispensed {units} units of {med.name}"`.
3. Instantiate test medications and patients, simulate prescriptions, and print out the patient medical record and remaining stock.

> [!IMPORTANT]
## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master class definition, constructor initialization, instance vs class attributes, encapsulation, dunder representations, and class/static methods:

---

### 🟢 Tier 1: Class Basics & Instance State (Exercises 1–3)

#### 🔹 Exercise 1: Server Node Status Object
* **Goal**: Define `class ServerNode` with `hostname: str` and `ip: str`. Add a boolean `is_online: bool = True` in `__init__`.
* **Method**: `toggle_status()` flips the boolean and prints state.

#### 🔹 Exercise 2: Point 2D Geometric Distance
* **Goal**: Define `class Point` with `x: float` and `y: float`.
* **Method**: `distance_to(other: Point) -> float` calculates Euclidean distance $\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$.

#### 🔹 Exercise 3: String Representations (`__str__` and `__repr__`)
* **Goal**: Define `class Book` with `title: str`, `author: str`, and `isbn: str`.
* **Requirement**: Implement both `__str__` (e.g. `"<Title> by <Author>"`) and `__repr__` (e.g. `Book(title='...', ...)`).

---

### 🟡 Tier 2: State Mutation & Class Attributes (Exercises 4–6)

#### 🔹 Exercise 4: Bank Account with Deposit & Withdrawal Guards
* **Goal**: Define `class BankAccount` with `account_holder: str` and `balance: float = 0.0`.
* **Methods**: `deposit(amount: float)` (checks amount > 0) and `withdraw(amount: float)` (checks amount > 0 and amount <= balance; returns `bool`).

#### 🔹 Exercise 5: Global Class Instance Counter
* **Goal**: Define `class DatabaseConnection` with class attribute `ACTIVE_CONNECTIONS = 0`.
* **Requirement**: Increment counter on `__init__`, and implement a `close()` method that decrements counter and sets `self.connected = False`.

#### 🔹 Exercise 6: Encapsulated Wallet with Name Mangling
* **Goal**: Define `class DigitalWallet` with public `owner` and private `__secret_seed_phrase`.
* **Requirement**: Demonstrate that accessing `wallet.__secret_seed_phrase` raises an `AttributeError`, but can be read via a dedicated `reveal_seed(master_password: str)` method.

---

### 🟠 Tier 3: Factory Methods & Class Relationships (Exercises 7–9)

#### 🔹 Exercise 7: Alternative Constructor `@classmethod` Factory
* **Goal**: Define `class UserProfile` with `username`, `email`, `role`.
* **Requirement**: Implement `@classmethod from_csv_string(cls, raw_csv: str)` that splits `"alice,alice@co.com,admin"` and returns an instantiated object.

#### 🔹 Exercise 8: Static Method Validator `@staticmethod`
* **Goal**: Inside `class PasswordPolicy`, create `@staticmethod is_valid_password(password: str) -> bool` checking length and complexity without needing an instance.

#### 🔹 Exercise 9: Aggregated Order and Line-Item Composite System
* **Goal**: Define `class OrderItem` (`name`, `price`, `qty`) and `class ShoppingOrder` containing a list of `OrderItem` objects.
* **Method**: `order.calculate_total()` sums item costs and returns formatted receipt.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Hospital Pharmacy Dispenser & Allergy Guard System
* **Goal**: Multi-class domain architecture linking `Medication` inventory state with `Patient` medical charts, allergy safety verification, and automated stock depletion.

---

## 📝 Quick Exercise: Hospital Pharmacy Prescription Dispenser & Allergy Safety Gate

### 🏢 Real-Life Scenario
You are developing the pharmacy dispensing subsystem for a hospital electronic health record (EHR). When a physician issues a medication prescription for an admitted patient, the dispenser module checks the patient's known allergy records, verifies that the pharmacy has sufficient unit stock in inventory, updates the patient's active prescription chart, and decrements physical shelf inventory.

### 📋 Requirements
1. **Define `Medication` class**:
   - `__init__(self, code: str, name: str, stock_units: int, unit_cost: float)`
   - Method `dispense(self, units: int) -> bool`: Deducts units if `0 < units <= self.stock_units` and returns `True`; otherwise returns `False`.
   - Method `restock(self, units: int) -> None`: Increments `stock_units`.
   - Method `__str__(self) -> str`: Formats inventory summary.
2. **Define `Patient` class**:
   - `__init__(self, patient_id: str, name: str, allergies: list[str] = None)`: Initializes allergy set and an empty prescriptions list.
   - Method `prescribe(self, med: Medication, units: int) -> tuple[bool, str]`:
     - Inspect patient allergies. If any allergy keyword is found inside `med.name.lower()`, return `False, "ALLERGY ALERT: Patient is allergic to this medication!"`.
     - Attempt to dispense from `med.dispense(units)`. If stock is insufficient, return `False, "INVENTORY ERROR: Insufficient pharmacy stock"`.
     - If safe and in stock, add medication name to `self.prescriptions` and return `True, f"Successfully dispensed {units} units of {med.name}"`.
3. Instantiate test medications and patients, simulate prescriptions, and print out the patient medical record and remaining stock.

> [!IMPORTANT]
> **Cumulative Level 1 Milestone Constraint**: Combine concepts from **Lessons 1 through 10** (variables, types, input/output, casting, operators, conditionals, loops, lists, sets, dicts, functions, exception safety, and OOP classes/methods).

### 🎯 Expected Output
```text
==================================================
           HOSPITAL PHARMACY DISPENSER            
==================================================
Rx #1: ✅ Successfully dispensed 10 units of Amoxicillin 500mg
Rx #2: ❌ ALLERGY ALERT: Patient is allergic to this medication!
Rx #3: ❌ INVENTORY ERROR: Insufficient pharmacy stock
--------------------------------------------------
PATIENT MEDICAL RECORD:
Patient ID:       PAT-409
Patient Name:     Sarah Connor
Known Allergies:  aspirin, ibuprofen
Active Prescriptions: Amoxicillin 500mg
--------------------------------------------------
UPDATED PHARMACY INVENTORY:
  - [MED-01] Amoxicillin 500mg - Stock: 40 units ($12.50/unit)
  - [MED-02] Aspirin 100mg - Stock: 100 units ($4.00/unit)
  - [MED-03] Ibuprofen 200mg - Stock: 5 units ($6.00/unit)
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Hospital & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Hospital Pharmacy Dispenser
# =====================================================================
class Medication:
    def __init__(self, code: str, name: str, stock_units: int, unit_cost: float):
        self.code = code
        self.name = name
        self.stock_units = stock_units
        self.unit_cost = unit_cost

    def dispense(self, units: int) -> bool:
        if 0 < units <= self.stock_units:
            self.stock_units -= units
            return True
        return False

    def restock(self, units: int) -> None:
        if units > 0:
            self.stock_units += units

    def __str__(self) -> str:
        return f"[{self.code}] {self.name} - Stock: {self.stock_units} units (${self.unit_cost:.2f}/unit)"


class Patient:
    def __init__(self, patient_id: str, name: str, allergies: list[str] = None):
        self.patient_id = patient_id
        self.name = name
        self.allergies = {a.lower() for a in allergies} if allergies else set()
        self.prescriptions = []

    def prescribe(self, med: Medication, units: int) -> tuple[bool, str]:
        for allergy in self.allergies:
            if allergy in med.name.lower():
                return False, f"ALLERGY ALERT: Patient is allergic to this medication!"

        if not med.dispense(units):
            return False, "INVENTORY ERROR: Insufficient pharmacy stock"

        self.prescriptions.append(med.name)
        return True, f"Successfully dispensed {units} units of {med.name}"


med1 = Medication("MED-01", "Amoxicillin 500mg", stock_units=50, unit_cost=12.50)
med2 = Medication("MED-02", "Aspirin 100mg", stock_units=100, unit_cost=4.00)
med3 = Medication("MED-03", "Ibuprofen 200mg", stock_units=5, unit_cost=6.00)

patient = Patient("PAT-409", "Sarah Connor", allergies=["aspirin", "ibuprofen"])

print("==================================================")
print("           HOSPITAL PHARMACY DISPENSER            ")
print("==================================================")

ok1, msg1 = patient.prescribe(med1, 10)
print(f"Rx #1: {'✅' if ok1 else '❌'} {msg1}")

ok2, msg2 = patient.prescribe(med2, 5)
print(f"Rx #2: {'✅' if ok2 else '❌'} {msg2}")

ok3, msg3 = patient.prescribe(med3, 20)
print(f"Rx #3: {'✅' if ok3 else '❌'} {msg3}")

print("--------------------------------------------------")
print("PATIENT MEDICAL RECORD:")
print(f"Patient ID:       {patient.patient_id}")
print(f"Patient Name:     {patient.name}")
print(f"Known Allergies:  {', '.join(sorted(patient.allergies))}")
print(f"Active Prescriptions: {', '.join(patient.prescriptions) if patient.prescriptions else 'None'}")
print("--------------------------------------------------")
print("UPDATED PHARMACY INVENTORY:")
for m in (med1, med2, med3):
    print(f"  - {m}")
print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
class ServerNode:
    def __init__(self, hostname: str, ip: str):
        self.hostname, self.ip, self.is_online = hostname, ip, True
    def toggle_status(self): self.is_online = not self.is_online

# Ex 2:
class Point:
    def __init__(self, x: float, y: float): self.x, self.y = x, y
    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

# Ex 3:
class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title, self.author, self.isbn = title, author, isbn
    def __str__(self): return f"'{self.title}' by {self.author}"
    def __repr__(self): return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"

# Ex 4:
class BankAccount:
    def __init__(self, holder: str, balance: float = 0.0):
        self.holder, self.balance = holder, balance
    def deposit(self, amt: float):
        if amt > 0: self.balance += amt
    def withdraw(self, amt: float) -> bool:
        if 0 < amt <= self.balance:
            self.balance -= amt
            return True
        return False

# Ex 5:
class DatabaseConnection:
    ACTIVE = 0
    def __init__(self):
        DatabaseConnection.ACTIVE += 1
        self.connected = True
    def close(self):
        if self.connected:
            DatabaseConnection.ACTIVE -= 1
            self.connected = False

# Ex 6:
class DigitalWallet:
    def __init__(self, owner: str, seed: str):
        self.owner = owner
        self.__secret_seed_phrase = seed
    def reveal_seed(self, pw: str):
        return self.__secret_seed_phrase if pw == "admin123" else "Access Denied"

# Ex 7:
class UserProfile:
    def __init__(self, username: str, email: str, role: str):
        self.username, self.email, self.role = username, email, role
    @classmethod
    def from_csv_string(cls, raw: str):
        u, e, r = raw.split(",")
        return cls(u.strip(), e.strip(), r.strip())

# Ex 8:
class PasswordPolicy:
    @staticmethod
    def is_valid_password(pw: str) -> bool:
        return len(pw) >= 8 and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw)

# Ex 9:
class OrderItem:
    def __init__(self, name: str, price: float, qty: int):
        self.name, self.price, self.qty = name, price, qty
    @property
    def line_total(self): return self.price * self.qty

class ShoppingOrder:
    def __init__(self): self.items: list[OrderItem] = []
    def add_item(self, item: OrderItem): self.items.append(item)
    def calculate_total(self) -> float: return sum(i.line_total for i in self.items)
```
</details>

