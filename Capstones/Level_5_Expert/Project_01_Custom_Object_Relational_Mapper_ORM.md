# Capstone Project 5.1: Declarative Metaclass-Powered ORM

## 📌 Project Overview
Design and build a zero-dependency **Declarative Object-Relational Mapper (ORM)** and Schema Validation Engine from scratch (similar to Django ORM or Peewee) utilizing CPython Metaclasses (`__prepare__`, `__new__`), custom Data Descriptors (`__get__`, `__set__`, `__delete__`), `__slots__` memory optimization, dirty-field tracking, and dynamic SQL query generators with operator overloading.

---

## 🎯 Learning Objectives
- **CPython Metaclasses**: Intercepting class creation with `__prepare__` (to preserve attribute declaration order) and `__new__` (to introspect and register model schema fields).
- **Python Descriptor Protocol**: Implementing typed field descriptors (`IntegerField`, `CharField`, `BooleanField`, `ForeignKey`) that enforce runtime type checks and handle nullable/default constraints.
- **Memory Optimization with `__slots__`**: Dynamically configuring `__slots__` during class creation to eliminate `__dict__` overhead and reduce model instance memory consumption by $>60\%$.
- **Operator Overloading for SQL Generation**: Overloading comparison dunders (`__eq__`, `__gt__`, `__lt__`, `__contains__`) on field descriptors to compile pythonic query expressions into parameterized SQL queries (`User.age > 21` $\to$ `"age > %s", [21]`).
- **Dirty State Tracking**: Tracking modified attributes on instances to generate selective `UPDATE` statements containing only altered columns.

---

## 🏗️ System Architecture

```text
       +------------------------------------+
       |          ModelMetaclass            |
       |  (__prepare__, __new__, __init__)  |
       +------------------------------------+
                         |
      +------------------+------------------+
      |                                     |
+--------------------+              +--------------------+
|     BaseModel      |              |   FieldDescriptor  |
+--------------------+              +--------------------+
| - _is_dirty: set   |              | - column_name: str |
| - _original_state  |              | - data_type: type  |
| + save()           |              | - primary_key: bool|
| + delete()         |              | + __get__()        |
| + query()          |              | + __set__()        |
+--------------------+              | + __eq__(), __gt__()
                                    +--------------------+
```

---

## 📋 Functional Requirements

### 1. Descriptor Protocol for Model Fields
Implement field classes conforming to the Descriptor protocol:
- `Field`: Base descriptor managing column naming and nullability.
- `CharField(max_length: int = 255, default: str = "")`
- `IntegerField(min_value: int = None, max_value: int = None)`
- `BooleanField(default: bool = False)`
- `ForeignKey(to_model: type, on_delete: str = "CASCADE")`

### 2. Metaclass `ModelMeta`
- Preserves field order using `__prepare__`.
- Collects all `Field` instances into a `_fields` mapping on the model class.
- Generates `CREATE TABLE IF NOT EXISTS` DDL statements automatically.
- Automatically generates `__slots__` on the class containing all field names plus internal tracking flags.

### 3. Declarative Model Definition API
Enable clean declarative models:
```python
class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(max_length=50)
    age = IntegerField(min_value=0)
    is_active = BooleanField(default=True)
```

### 4. QuerySet Builder & Operator Overloading
Support natural Python expression filtering:
```python
# Should compile to: SELECT id, username, age, is_active FROM user WHERE age >= ? AND is_active = ?
users = User.objects.filter((User.age >= 18) & (User.is_active == True)).execute()
```

### 5. Dirty Field Tracking on `save()`
If only `user.username` is modified, executing `user.save()` generates:
`UPDATE user SET username = ? WHERE id = ?` (avoiding rewriting unchanged columns).

---

## 📐 Phased Implementation Guide

### Phase 1: Field Descriptors with Expression Nodes
```python
class ExpressionNode:
    def __init__(self, column: str, op: str, value: any):
        self.column = column
        self.op = op
        self.value = value

    def to_sql(self) -> tuple[str, list]:
        return f"{self.column} {self.op} ?", [self.value]

class Field:
    def __init__(self, primary_key: bool = False, nullable: bool = False, default=None):
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
        self.name = None  # Bound by Metaclass

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._values.get(self.name, self.default)

    def __set__(self, instance, value):
        if value is None and not self.nullable and not self.primary_key:
            raise ValueError(f"Field '{self.name}' cannot be None.")
        instance._values[self.name] = value
        instance._dirty_fields.add(self.name)

    def __eq__(self, value) -> ExpressionNode:
        return ExpressionNode(self.name, "=", value)

    def __gt__(self, value) -> ExpressionNode:
        return ExpressionNode(self.name, ">", value)
```

### Phase 2: Model Metaclass & BaseModel
```python
class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
                
        attrs["_fields"] = fields
        cls = super().__new__(mcs, name, bases, attrs)
        return cls

class BaseModel(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        self._values = {}
        self._dirty_fields = set()
        for key, field in self._fields.items():
            if key in kwargs:
                setattr(self, key, kwargs[key])
            elif field.default is not None:
                setattr(self, key, field.default)
```

### Phase 3: DDL Generation & SQLite Connection Bridge
Implement database binding and schema migration methods.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Type Violation** | Assign `user.age = "twenty"` | Raises `TypeError` via descriptor validation before touching database |
| **Selective Dirty Update** | Change only `user.username`, call `save()` | Generated SQL contains only `username` in `SET` clause |
| **Primary Key Protection** | Attempt to modify primary key of saved record | Raises `AttributeError` or prevents corrupting database identity |
| **Memory Profiling** | Allocate 100,000 model instances | Instances with `__slots__` use $< 50\%$ RAM compared to dict instances |

---

## 🚀 Bonus Challenges
- **Lazy Foreign Key Resolution**: Accessing `post.author` dynamically fetches the related `User` record on first access and caches it.
- **Migration Generator**: Compare declarative model state with live database SQLite `PRAGMA table_info` and auto-generate `ALTER TABLE` statements.
