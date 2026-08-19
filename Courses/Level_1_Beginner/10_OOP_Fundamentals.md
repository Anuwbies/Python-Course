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

## 4. String Representations: `__str__` and `__repr__`

By default, printing an object outputs its raw memory pointer (`<__main__.Employee object at 0x7f8a10>`). Implementing special representation methods makes objects readable and easy to debug:

```python
class Product:
    def __init__(self, sku: str, name: str, price: float):
        self.sku = sku
        self.name = name
        self.price = price

    # __str__: User-friendly string for print() and str()
    def __str__(self) -> str:
        return f"{self.name} (${self.price:.2f}) [{self.sku}]"

    # __repr__: Unambiguous developer representation
    def __repr__(self) -> str:
        return f"Product(sku='{self.sku}', name='{self.name}', price={self.price})"

item = Product("SKU-99", "Mechanical Keyboard", 129.99)
print(item)        # Calls __str__ -> Mechanical Keyboard ($129.99) [SKU-99]
print(repr(item))  # Calls __repr__ -> Product(sku='SKU-99', name='Mechanical Keyboard', price=129.99)
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
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Medication Domain Class (Lessons 1-10)
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


# 2. Patient Domain Class (Lessons 1-10)
class Patient:
    def __init__(self, patient_id: str, name: str, allergies: list[str] = None):
        self.patient_id = patient_id
        self.name = name
        self.allergies = {a.lower() for a in allergies} if allergies else set()
        self.prescriptions = []

    def prescribe(self, med: Medication, units: int) -> tuple[bool, str]:
        # Check allergy safety (Lessons 4 & 7)
        for allergy in self.allergies:
            if allergy in med.name.lower():
                return False, f"ALLERGY ALERT: Patient is allergic to this medication!"

        # Attempt pharmacy inventory depletion (Lesson 10)
        if not med.dispense(units):
            return False, "INVENTORY ERROR: Insufficient pharmacy stock"

        self.prescriptions.append(med.name)
        return True, f"Successfully dispensed {units} units of {med.name}"


# 3. Execution Simulation
med1 = Medication("MED-01", "Amoxicillin 500mg", stock_units=50, unit_cost=12.50)
med2 = Medication("MED-02", "Aspirin 100mg", stock_units=100, unit_cost=4.00)
med3 = Medication("MED-03", "Ibuprofen 200mg", stock_units=5, unit_cost=6.00)

patient = Patient("PAT-409", "Sarah Connor", allergies=["aspirin", "ibuprofen"])

print("==================================================")
print("           HOSPITAL PHARMACY DISPENSER            ")
print("==================================================")

# Test 1: Safe antibiotic prescription
ok1, msg1 = patient.prescribe(med1, 10)
print(f"Rx #1: {'✅' if ok1 else '❌'} {msg1}")

# Test 2: Known allergy trigger
ok2, msg2 = patient.prescribe(med2, 5)
print(f"Rx #2: {'✅' if ok2 else '❌'} {msg2}")

# Test 3: Insufficient inventory request (requesting 20, only 5 available)
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
```

**Explanation of the Solution:**
- `Medication` encapsulates stock state and guarantees that units cannot be dispensed if requested counts exceed available inventory.
- `Patient` safeguards medication administration by checking incoming drug names against the patient's allergy set.
- All 10 lessons of Level 1 (types, variables, operators, conditionals, loops, sequences, sets, dicts, functions, and OOP classes) work together in a unified system.
</details>
