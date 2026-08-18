# Lesson 10: Object-Oriented Programming (OOP) Fundamentals

Object-Oriented Programming (OOP) is a programming paradigm that organizes code into **Objects**, which combine **State** (attributes/data) and **Behavior** (methods/functions).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the difference between a **Class** (blueprint) and an **Object** (instance).
2. Initialize objects using the `__init__` constructor method.
3. Understand the role of the `self` keyword.
4. Implement instance methods that modify and read internal state.
5. Create user-friendly string representations using `__str__`.

---

## 1. Classes vs Objects

- **Class**: A blueprint or template for creating objects (e.g. `BankAccount` blueprint).
- **Object**: A concrete instance created from that blueprint (e.g. `alice_account`, `bob_account`).

```python
class Dog:
    # The Constructor method: initializes instance attributes
    def __init__(self, name, breed, age):
        self.name = name    # Instance attribute
        self.breed = breed  # Instance attribute
        self.age = age      # Instance attribute

    # Instance method (behavior)
    def bark(self):
        print(f"{self.name} says: Woof! Woof!")

# Instantiating objects:
dog1 = Dog("Buddy", "Golden Retriever", 3)
dog2 = Dog("Bella", "Poodle", 2)

dog1.bark() # Buddy says: Woof! Woof!
print(f"{dog2.name} is {dog2.age} years old.")
```

---

## 2. What is `self`?

- `self` refers to the **specific instance** of the class currently being operated on.
- When you call `dog1.bark()`, Python behind the scenes converts it to `Dog.bark(dog1)`.

---

## 3. Building a Real Class: Bank Account

```python
class BankAccount:
    def __init__(self, account_number, holder_name, balance=0.0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = float(balance)

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive!")
            return False
        self.balance += amount
        print(f"Deposited ${amount:.2f}. New Balance: ${self.balance:.2f}")
        return True

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"❌ Insufficient funds! Current balance: ${self.balance:.2f}")
            return False
        if amount <= 0:
            print("Withdrawal must be positive!")
            return False
        self.balance -= amount
        print(f"Withdrew ${amount:.2f}. Remaining Balance: ${self.balance:.2f}")
        return True

    # Magic dunder method for pretty printing
    def __str__(self):
        return f"Account[{self.account_number}]: {self.holder_name} | Balance: ${self.balance:.2f}"
```

### Using the Bank Account Class:
```python
acc = BankAccount("ACC-101", "Alex Smith", 250.0)
print(acc)  # Calls __str__ automatically

acc.deposit(100.0)
acc.withdraw(50.0)
acc.withdraw(500.0) # Correctly rejects due to insufficient funds!
```

---

## 📝 Quick Exercise

**Prompt**:
Create a `Student` class:
1. `__init__(self, name, student_id)`: Initializes name, student_id, and an empty list of `grades = []`.
2. `add_grade(self, grade)`: Appends grade to list if between `0` and `100`.
3. `get_average(self)`: Computes and returns the average grade.
4. `__str__(self)`: Returns `f"Student: {name} (ID: {student_id}) - GPA: {average:.2f}"`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
class Student:
    def __init__(self, name: str, student_id: str):
        self.name = name
        self.student_id = student_id
        self.grades = []

    def add_grade(self, grade: float) -> bool:
        if 0 <= grade <= 100:
            self.grades.append(float(grade))
            return True
        print(f"Invalid grade {grade}. Must be between 0 and 100.")
        return False

    def get_average(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def __str__(self) -> str:
        return f"Student: {self.name} (ID: {self.student_id}) - Average: {self.get_average():.2f}%"

# Example Usage:
s = Student("Sarah Jenkins", "S1094")
s.add_grade(95)
s.add_grade(88)
s.add_grade(92)
print(s) # Student: Sarah Jenkins (ID: S1094) - Average: 91.67%
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is the purpose of `__init__` in a Python class?**
   - A) To delete objects from memory
   - B) To initialize attributes when a new instance is instantiated
   - C) To run a loop
   - D) To import external modules

2. **Why must instance methods in Python have `self` as their first parameter?**
   - A) To pass the reference of the calling instance object
   - B) It is optional and can be omitted
   - C) `self` is a special variable reserved for numbers
   - D) To make the method static

3. **What method is automatically invoked when you pass an object to `print(my_object)`?**
   - A) `__init__`
   - B) `__str__`
   - C) `__len__`
   - D) `__call__`

<details>
<summary><b>View Answers</b></summary>
1: B (Constructor initializes object state)<br>
2: A (Provides access to the instance's attributes and methods)<br>
3: B (__str__ produces the readable string representation)
</details>
