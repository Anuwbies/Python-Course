# Lesson 10: Object-Oriented Programming (OOP) Fundamentals

Object-Oriented Programming (OOP) is a fundamental programming paradigm that organizes complex software by bundling **State** (attributes and data) and **Behavior** (methods and operations) together into modular units called **Objects**.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the core principles of OOP: **Encapsulation**, **State**, and **Behavior**.
2. Differentiate between a **Class** (the blueprint/type) and an **Object** (the concrete instance).
3. Initialize object state using the `__init__` constructor method.
4. Master the `self` parameter and Python's instance binding mechanism.
5. Distinguish between **Instance Attributes** and **Class Attributes**.
6. Implement state-mutating instance methods with built-in validation checks.
7. Customize readable string representations using the `__str__` dunder method.
8. Design collaborative multi-object systems (e.g. manager classes coordinating collections of objects).

---

## 1. Classes vs. Objects: The Blueprint Model

- **Class**: A user-defined data type and structural blueprint defining what data an entity stores and what operations it can perform (e.g., `BankAccount`, `UserAccount`, `DeliveryVehicle`).
- **Object (Instance)**: A concrete, independent entity instantiated in computer memory based on that blueprint.

```
       [ CLASS: BankAccount ]  <--- Blueprint
                 │
   ┌─────────────┴─────────────┐
   ▼                           ▼
[ Object 1: acc_alice ]     [ Object 2: acc_bob ]
owner: "Alice"              owner: "Bob"
balance: $2,500.00          balance: $140.00
```

---

## 2. Defining Classes, `__init__`, and `self`

The `__init__` method (called the **Constructor**) executes automatically whenever a new object is created. Its purpose is to initialize the instance's unique attributes.

```python
class ServerNode:
    # Constructor:
    def __init__(self, hostname: str, ip_address: str, ram_gb: int):
        # self.attribute_name binds the data to THIS specific instance:
        self.hostname = hostname
        self.ip_address = ip_address
        self.ram_gb = ram_gb
        self.is_online = False  # Default initial state

    # Instance method:
    def boot(self):
        self.is_online = True
        print(f"🚀 Server {self.hostname} ({self.ip_address}) is now ONLINE.")

# Instantiating objects:
node1 = ServerNode("web-prod-01", "10.0.0.1", 32)
node2 = ServerNode("db-primary-01", "10.0.0.2", 128)

node1.boot()
print(f"{node2.hostname} has {node2.ram_gb} GB RAM. Online: {node2.is_online}")
```

### 🔍 Demystifying `self`
- `self` is a reference to the **specific instance** that invoked the method.
- When you execute `node1.boot()`, Python behind the scenes translates it to `ServerNode.boot(node1)`.
- `self` allows methods on an object to read and mutate that specific object's private memory state.

---

## 3. Instance Attributes vs. Class Attributes

- **Instance Attributes**: Bound to `self`. Each object possesses its own independent copy (e.g. `self.balance`).
- **Class Attributes**: Defined directly inside the class body outside any method. Shared equally by **all** instances of the class.

```python
class Employee:
    # Class Attribute (Shared by all employees):
    company_name = "Apex Global Technologies"
    annual_bonus_rate = 0.08

    def __init__(self, name: str, salary: float):
        # Instance Attributes (Unique per employee):
        self.name = name
        self.salary = salary

emp1 = Employee("Sarah Connor", 95000.0)
emp2 = Employee("Marcus Vance", 85000.0)

print(emp1.company_name)  # 'Apex Global Technologies'
print(emp2.company_name)  # 'Apex Global Technologies'
```

---

## 4. The Magic `__str__` Dunder Method

By default, passing an object to `print(node1)` prints an unhelpful memory address like `<__main__.ServerNode object at 0x7f8a1b>`.

Implementing the `__str__(self)` dunder (*double underscore*) method tells Python how to format the object as a user-friendly string:

```python
class BankAccount:
    def __init__(self, account_id: str, owner: str, initial_deposit: float = 0.0):
        self.account_id = account_id
        self.owner = owner
        self.balance = float(initial_deposit)

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            print("[ERROR] Deposit must be positive.")
            return False
        self.balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        if amount <= 0 or amount > self.balance:
            print("[ERROR] Invalid or insufficient funds.")
            return False
        self.balance -= amount
        return True

    # User-facing string representation:
    def __str__(self) -> str:
        return f"BankAccount[{self.account_id}] Owner: {self.owner:<15} | Balance: ${self.balance:,.2f}"

acc = BankAccount("ACC-902", "Elena Rostova", 1500.00)
print(acc)  # Output: BankAccount[ACC-902] Owner: Elena Rostova   | Balance: $1,500.00
```

---

## 5. Object Collaboration: Multi-Class Architectures

In real systems, objects interact with and contain collections of other objects:

```python
class Department:
    def __init__(self, department_name: str):
        self.department_name = department_name
        self.members = []  # List holding Employee objects

    def add_employee(self, emp: Employee):
        self.members.append(emp)

    def calculate_total_payroll(self) -> float:
        return sum(emp.salary for emp in self.members)
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_10_OOP_Fundamentals.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Testing/Level_1_Beginner/Lesson_10_OOP_Fundamentals.py):

```python
# Student Course Registry System
class Course:
    def __init__(self, course_code: str, title: str, max_capacity: int = 30):
        self.course_code = course_code
        self.title = title
        self.max_capacity = max_capacity
        self.enrolled_students = []

    def enroll(self, student_name: str) -> bool:
        if len(self.enrolled_students) >= self.max_capacity:
            print(f"[ERROR] Cannot enroll {student_name}: Course {self.course_code} is FULL.")
            return False
        self.enrolled_students.append(student_name)
        return True

    def __str__(self) -> str:
        return f"[{self.course_code}] {self.title} - Enrolled: {len(self.enrolled_students)}/{self.max_capacity}"

cs101 = Course("CS-101", "Intro to Python Programming", max_capacity=2)
cs101.enroll("Alex")
cs101.enroll("Maria")
cs101.enroll("Jordan")  # Exceeds capacity!
print(cs101)
```

---

## 📝 Quick Exercise: Commercial Fleet Logistics & Telematics System

### 🏢 Real-Life Scenario
You are developing the fleet tracking and telematics management engine for a regional parcel logistics company. The company needs an Object-Oriented system comprising a `DeliveryVehicle` class (modeling vehicle odometer, fuel capacity, fuel consumption, trip tracking, and maintenance alerts) and a `FleetManager` class (coordinating vehicles across the depot and producing executive fleet status summaries).

### 📋 Requirements
1. Create a `DeliveryVehicle` class:
   - **`__init__(self, vehicle_id: str, model: str, max_payload_kg: float, fuel_capacity_l: float)`**:
     - `self.vehicle_id = vehicle_id`
     - `self.model = model`
     - `self.max_payload_kg = float(max_payload_kg)`
     - `self.fuel_capacity_l = float(fuel_capacity_l)`
     - `self.current_fuel_l = float(fuel_capacity_l)` (starts with a full tank)
     - `self.odometer_km = 0.0`
     - `self.trip_count = 0`
     - `self.maintenance_due = False`
   - **`refuel(self, liters: float) -> float`**:
     - If `liters <= 0`: print error `"[ERROR] Refuel amount must be positive."` and return `self.current_fuel_l`.
     - Adds `liters`, capping at `self.fuel_capacity_l`.
     - Returns `self.current_fuel_l`.
   - **`record_trip(self, distance_km: float, fuel_consumed_l: float) -> bool`**:
     - If `distance_km <= 0` or `fuel_consumed_l <= 0`:
       - Print `"[ERROR] Invalid trip metrics."` and return `False`.
     - If `fuel_consumed_l > self.current_fuel_l`:
       - Print `f"[ERROR] Insufficient Fuel in {self.vehicle_id} for trip!"` and return `False`.
     - Deduct `fuel_consumed_l` from `self.current_fuel_l`.
     - Add `distance_km` to `self.odometer_km`.
     - Increment `self.trip_count += 1`.
     - If `self.odometer_km >= 500.0`: set `self.maintenance_due = True`.
     - Return `True`.
   - **`__str__(self) -> str`**:
     - Returns formatted status string:
       `f"[{self.vehicle_id}] {self.model:<18} | Odo: {self.odometer_km:>6.1f} km | Fuel: {self.current_fuel_l:>5.1f}/{self.fuel_capacity_l:.1f} L | Trips: {self.trip_count} | Maint Due: {self.maintenance_due}"`

2. Create a `FleetManager` class:
   - **`__init__(self, depot_name: str)`**:
     - `self.depot_name = depot_name`
     - `self.vehicles = []`
   - **`add_vehicle(self, vehicle: DeliveryVehicle) -> None`**:
     - Appends `vehicle` to `self.vehicles`.
   - **`print_fleet_report(self) -> None`**:
     - Iterates through all vehicles and displays each vehicle's `__str__`.
     - Computes and displays fleet aggregates: total fleet vehicles, total cumulative km driven, total completed trips, and a list of vehicle IDs currently requiring maintenance.

3. Test the fleet:
   - Instantiate `FleetManager("Northwest Regional Depot")`.
   - Add 3 vehicles:
     - `DeliveryVehicle("VAN-101", "Ford Transit High", 1500, 75.0)`
     - `DeliveryVehicle("VAN-102", "Mercedes Sprinter", 1800, 85.0)`
     - `DeliveryVehicle("EV-201", "Rivian Delivery Van", 1200, 100.0)`
   - Record trips on the vehicles (simulate trips so at least one exceeds 500 km).
   - Display the comprehensive depot fleet report.

> [!IMPORTANT]
> **Strict Constraint**: Use **only** concepts covered across Lessons 1 through 10 (variables, primitives, strings, conditionals, loops, lists, dicts, functions, OOP classes, methods, `__init__`, `self`, `__str__`, collections of objects, f-strings, and `print()`).

### 🎯 Expected Output
```text
================================================================================
           FLEET TELEMATICS REPORT - Northwest Regional Depot                   
================================================================================
VEHICLE STATUS LEDGER:
- [VAN-101] Ford Transit High   | Odo:  520.0 km | Fuel:  25.0/75.0 L | Trips: 2 | Maint Due: True
- [VAN-102] Mercedes Sprinter   | Odo:  310.5 km | Fuel:  50.0/85.0 L | Trips: 1 | Maint Due: False
- [EV-201 ] Rivian Delivery Van | Odo:  180.0 km | Fuel:  65.0/100.0 L | Trips: 1 | Maint Due: False
--------------------------------------------------------------------------------
FLEET-WIDE AGGREGATES:
Total Fleet Vehicles:   3 vans
Total Cumulative Range: 1,010.5 km
Total Completed Trips:  4 trips
Maintenance Due List:   ['VAN-101']
================================================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
class DeliveryVehicle:
    """Represents a commercial delivery vehicle tracking telemetry and maintenance."""
    
    def __init__(self, vehicle_id: str, model: str, max_payload_kg: float, fuel_capacity_l: float):
        self.vehicle_id = vehicle_id
        self.model = model
        self.max_payload_kg = float(max_payload_kg)
        self.fuel_capacity_l = float(fuel_capacity_l)
        self.current_fuel_l = float(fuel_capacity_l)
        self.odometer_km = 0.0
        self.trip_count = 0
        self.maintenance_due = False

    def refuel(self, liters: float) -> float:
        """Adds fuel to tank, capping at max capacity."""
        if liters <= 0:
            print("[ERROR] Refuel amount must be positive.")
            return self.current_fuel_l
        self.current_fuel_l = min(self.current_fuel_l + liters, self.fuel_capacity_l)
        return self.current_fuel_l

    def record_trip(self, distance_km: float, fuel_consumed_l: float) -> bool:
        """Validates and records a delivery route trip."""
        if distance_km <= 0 or fuel_consumed_l <= 0:
            print("[ERROR] Invalid trip metrics.")
            return False
            
        if fuel_consumed_l > self.current_fuel_l:
            print(f"[ERROR] Insufficient fuel in {self.vehicle_id} for requested trip!")
            return False

        self.current_fuel_l -= fuel_consumed_l
        self.odometer_km += distance_km
        self.trip_count += 1
        
        if self.odometer_km >= 500.0:
            self.maintenance_due = True
            
        return True

    def __str__(self) -> str:
        return (
            f"[{self.vehicle_id:<7}] {self.model:<19} | "
            f"Odo: {self.odometer_km:>6.1f} km | "
            f"Fuel: {self.current_fuel_l:>5.1f}/{self.fuel_capacity_l:.1f} L | "
            f"Trips: {self.trip_count} | "
            f"Maint Due: {self.maintenance_due}"
        )


class FleetManager:
    """Manages a collection of delivery vehicles for a regional logistics depot."""
    
    def __init__(self, depot_name: str):
        self.depot_name = depot_name
        self.vehicles = []

    def add_vehicle(self, vehicle: DeliveryVehicle) -> None:
        """Registers a delivery vehicle into the fleet."""
        self.vehicles.append(vehicle)

    def print_fleet_report(self) -> None:
        """Displays formatted operational status report across the entire fleet."""
        total_fleet_km = sum(v.odometer_km for v in self.vehicles)
        total_trips = sum(v.trip_count for v in self.vehicles)
        maint_list = [v.vehicle_id for v in self.vehicles if v.maintenance_due]

        print("================================================================================")
        print(f"           FLEET TELEMATICS REPORT - {self.depot_name}")
        print("================================================================================")
        print("VEHICLE STATUS LEDGER:")
        for v in self.vehicles:
            print(f"- {v}")
            
        print("--------------------------------------------------------------------------------")
        print("FLEET-WIDE AGGREGATES:")
        print(f"Total Fleet Vehicles:   {len(self.vehicles)} vans")
        print(f"Total Cumulative Range: {total_fleet_km:,.1f} km")
        print(f"Total Completed Trips:  {total_trips} trips")
        print(f"Maintenance Due List:   {maint_list}")
        print("================================================================================")


# Execution & Testing
depot = FleetManager("Northwest Regional Depot")

v1 = DeliveryVehicle("VAN-101", "Ford Transit High", 1500, 75.0)
v2 = DeliveryVehicle("VAN-102", "Mercedes Sprinter", 1800, 85.0)
v3 = DeliveryVehicle("EV-201", "Rivian Delivery Van", 1200, 100.0)

depot.add_vehicle(v1)
depot.add_vehicle(v2)
depot.add_vehicle(v3)

# Simulate trips
v1.record_trip(280.0, 25.0)
v1.record_trip(240.0, 25.0)  # Odometer reaches 520 km -> maintenance_due becomes True
v2.record_trip(310.5, 35.0)
v3.record_trip(180.0, 35.0)

# Display fleet summary
depot.print_fleet_report()
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is the purpose of `__init__` in a Python class?**
   - A) To destroy objects and reclaim memory.
   - B) To initialize attributes and state when a new object instance is created.
   - C) To define global variables.
   - D) To import external libraries.

2. **What does the `self` parameter represent in an instance method?**
   - A) A reference to the specific object instance invoking the method.
   - B) The parent Python interpreter.
   - C) A static copy of the class blueprint.
   - D) An optional keyword argument.

3. **What method is automatically called when you pass an object to `print(my_obj)`?**
   - A) `__init__`
   - B) `__repr__` or `__str__`
   - C) `__len__`
   - D) `__call__`

<details>
<summary><b>View Answers</b></summary>
1: B (Constructor initializes object state upon instantiation)<br>
2: A (self provides access to the instance's unique attributes and methods)<br>
3: B (__str__ produces the readable string representation for print())
</details>
