# Lesson 1: Advanced OOP: Inheritance, Polymorphism & super()

Welcome to Level 2! In this lesson, we level up our Object-Oriented Programming (OOP) skills by mastering how classes inherit attributes, override behaviors, dynamically resolve methods (MRO), and achieve true polymorphism.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Implement Single, Hierarchical, and Multiple Inheritance.
2. Use `super().__init__()` properly to delegate constructor execution.
3. Understand Method Overriding and Polymorphic interfaces.
4. Inspect and master the **Method Resolution Order (MRO)** algorithm (C3 Linearization).

---

## 1. Single & Hierarchical Inheritance

Inheritance models an **"is-a"** relationship (e.g., a `Manager` *is an* `Employee`). The child (derived) class inherits all methods and attributes from the parent (base) class.

```python
class Employee:
    def __init__(self, emp_id: str, name: str, base_salary: float):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = base_salary

    def calculate_pay(self) -> float:
        return self.base_salary

    def get_details(self) -> str:
        return f"[{self.emp_id}] {self.name} - Pay: ${self.calculate_pay():,.2f}"

# Child Class inherits from Employee
class Manager(Employee):
    def __init__(self, emp_id: str, name: str, base_salary: float, bonus: float):
        # Call the parent constructor safely using super()
        super().__init__(emp_id, name, base_salary)
        self.bonus = bonus

    # Method Overriding: replace parent calculate_pay with customized logic
    def calculate_pay(self) -> float:
        return self.base_salary + self.bonus

class Developer(Employee):
    def __init__(self, emp_id: str, name: str, base_salary: float, programming_language: str):
        super().__init__(emp_id, name, base_salary)
        self.programming_language = programming_language
```

---

## 2. Polymorphism in Practice

**Polymorphism** ("many forms") allows different classes to share the same method names while providing class-specific implementations. The caller doesn't need to know the exact child type:

```python
# A polymorphic function accepting ANY employee subclass
def print_payroll_summary(team: list[Employee]) -> None:
    print("=== 💼 COMPANY PAYROLL ===")
    for member in team:
        # Every object responds to .get_details() and .calculate_pay()
        print(member.get_details())

staff: list[Employee] = [
    Manager("M-01", "Alice Vance", 120_000, 25_000),
    Developer("D-01", "Gordon Freeman", 110_000, "Python"),
    Developer("D-02", "Eli Vance", 115_000, "Rust"),
]

print_payroll_summary(staff)
```

---

## 3. Multiple Inheritance & Method Resolution Order (MRO)

Python supports inheriting from multiple parent classes. When method names conflict, Python resolves which method to run using the **C3 Linearization (MRO)** algorithm.

```python
class LoggableMixin:
    def log(self, message: str) -> None:
        print(f"[AUDIT LOG] {self.__class__.__name__}: {message}")

class NotifiableMixin:
    def send_notification(self, recipient: str, message: str) -> None:
        print(f"📧 Sending notification to {recipient}: {message}")

# Inherits from Employee AND two reusable Mixin classes
class HRManager(Manager, LoggableMixin, NotifiableMixin):
    def conduct_review(self, target_employee: Employee) -> None:
        self.log(f"Review completed for {target_employee.name}")
        self.send_notification(target_employee.name, "Your review has been filed.")

# Inspecting the MRO (Resolution Order):
print(HRManager.mro())
# Output: [HRManager, Manager, Employee, LoggableMixin, NotifiableMixin, object]
```

---

## 📝 Quick Exercise

**Prompt**:
1. Create a base class `Vehicle` with attributes `make`, `model`, and method `start_engine()`.
2. Create an `ElectricCar` subclass inheriting from `Vehicle` that accepts a `battery_capacity_kwh` parameter and overrides `start_engine()` to output `"Starting silent electric motor..."`.
3. Create a `GasCar` subclass with `fuel_tank_liters` that overrides `start_engine()` to output `"Vroom! Engine roared to life."`.
4. Store multiple cars in a list and iterate through them calling `start_engine()` polymorphically.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
class Vehicle:
    def __init__(self, make: str, model: str):
        self.make = make
        self.model = model

    def start_engine(self) -> str:
        return f"{self.make} {self.model}: Engine started."

class ElectricCar(Vehicle):
    def __init__(self, make: str, model: str, battery_capacity_kwh: float):
        super().__init__(make, model)
        self.battery_capacity_kwh = battery_capacity_kwh

    def start_engine(self) -> str:
        return f"{self.make} {self.model} ({self.battery_capacity_kwh} kWh): Starting silent electric motor... ⚡"

class GasCar(Vehicle):
    def __init__(self, make: str, model: str, fuel_tank_liters: float):
        super().__init__(make, model)
        self.fuel_tank_liters = fuel_tank_liters

    def start_engine(self) -> str:
        return f"{self.make} {self.model} ({self.fuel_tank_liters}L): Vroom! Engine roared to life. 🔥"

# Polymorphism in action:
garage: list[Vehicle] = [
    ElectricCar("Tesla", "Model S", 100),
    GasCar("Ford", "Mustang GT", 60),
    ElectricCar("Porsche", "Taycan", 93.4)
]

for vehicle in garage:
    print(vehicle.start_engine())
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is the primary function of `super().__init__(...)` in a child class constructor?**
   - A) It deletes the child attributes
   - B) It executes the parent class initializer so inherited attributes are properly configured
   - C) It makes the class immutable
   - D) It imports standard libraries
   *(Answer: B)*

2. **How can you check if an object `obj` is an instance of a specific class or its subclasses?**
   - A) `type(obj) == ClassName`
   - B) `isinstance(obj, ClassName)`
   - C) `obj.is_class(ClassName)`
   - D) `issubclass(obj)`
   *(Answer: B)*

3. **What is the topmost root class of all classes in Python 3?**
   - A) `Base`
   - B) `type`
   - C) `object`
   - D) `Root`
   *(Answer: C)*
