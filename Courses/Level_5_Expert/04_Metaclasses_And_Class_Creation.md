# Lesson 4: Metaclasses & Dynamic Class Construction

In Python, classes themselves are objects. A **Metaclass** is the "class of a class" that defines how classes are constructed, validated, and registered at module load time.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand `type` as the default metaclass of all Python classes.
2. Construct classes dynamically at runtime using `type(name, bases, dict)`.
3. Intercept class creation using custom metaclasses inheriting from `type`.
4. Use modern `__init_subclass__` as an alternative to simple metaclasses.

---

## 1. Dynamic Class Construction with `type()`

```python
# Standard class definition:
class Robot:
    def speak(self):
        return "Beep boop"

# Creating the exact same class dynamically at runtime:
DynamicRobot = type(
    "DynamicRobot",
    (object,), # Base classes
    {"speak": lambda self: "Beep boop", "version": "2.0"} # Attributes/methods
)

bot = DynamicRobot()
print(bot.speak()) # Beep boop
```

---

## 2. Writing a Custom Metaclass for Class Validation

```python
class EnforceSnakeCaseMeta(type):
    """Metaclass that enforces all methods on subclasses use snake_case."""
    def __new__(mcs, name, bases, namespace):
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                if not attr_name.islower() or " " in attr_name:
                    raise TypeError(f"Method '{attr_name}' in class '{name}' violates snake_case convention!")
        return super().__new__(mcs, name, bases, namespace)

# Applying the metaclass
class APIClient(metaclass=EnforceSnakeCaseMeta):
    def fetch_data(self):
        return True

    # def FetchRecords(self): # ❌ Raises TypeError at module import time!
    #     pass
```

---

## 📝 Quick Exercise

**Prompt**:
Create an `AutoRegistryMeta` metaclass that automatically registers any subclass of `PluginBase` into a central dictionary `PLUGIN_REGISTRY[plugin_name] = cls`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
PLUGIN_REGISTRY = {}

class AutoRegistryMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != "PluginBase": # Don't register the root base class
            PLUGIN_REGISTRY[name] = cls
            print(f"🔌 Registered plugin: '{name}'")
        return cls

class PluginBase(metaclass=AutoRegistryMeta):
    pass

class AudioExportPlugin(PluginBase):
    pass

class VideoEncodingPlugin(PluginBase):
    pass

print(PLUGIN_REGISTRY) 
# Output: {'AudioExportPlugin': <class 'AudioExportPlugin'>, 'VideoEncodingPlugin': <class 'VideoEncodingPlugin'>}
```
</details>
