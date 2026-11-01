# Lesson 6: Dataclasses & Value Objects

**Prerequisites:** Levels 1–5 and Lessons 1–5 of this level. **Practice file:** `Practice/06_Dataclasses_And_Value_Objects.py`.

Use a data-focused object when named fields and value semantics express the model clearly. Generated convenience methods reduce repetition but do not replace validation or a decision about mutability.

## 1. Declare a record

The dataclass decorator reads annotated fields and generates methods such as initialization, repr, and equality according to its options. An annotation supplies field information; it still does not perform runtime type enforcement by itself.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Expense:
    category: str
    amount: int

expense = Expense("food", 120)
print(expense.category)
print(expense.amount)
```

This object represents a value rather than a service with a changing workflow. Equality compares generated field values by default, which is a useful choice for many records but not automatically the right identity model for every database entity.

## 2. Validate after generated initialization

`__post_init__` is called by the generated initializer after the field assignments. Use it to reject blank categories, Boolean/negative amounts, or other violated invariants. A frozen dataclass prevents ordinary field reassignment after construction; validation must still reject bad initial state.

Frozen does not recursively freeze nested objects. A frozen field containing a list still refers to a mutable list unless you choose a different representation. For an expense containing only a string and integer, those field values are already immutable.

## 3. Give mutable fields a factory

For a mutable collection field, `field(default_factory=list)` creates a new list for each initialized instance. A shared mutable default would reintroduce the ownership problem from earlier lessons. The factory is a callable supplied for later invocation, not an already-created list.

Use a tuple when a collection should represent an immutable fixed sequence, and document any nested mutability. Dataclass convenience should make those choices clearer rather than hide them.

## 4. Choose a value object or a behavior object

An Expense can describe data; an ExpenseService can validate workflows and use storage. A Library can hold changing loans while a Book record describes a catalog value. Not every class should be a dataclass, and adding the decorator does not automatically produce a complete domain design.

Review the generated representation and equality behavior as part of the public interface. Tests should focus on fields and intended semantics, not on incidental memory addresses or a repr chosen only for visual decoration.

References: [Dataclasses](https://docs.python.org/3.13/library/dataclasses.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict equality for two independently constructed identical expense values.
2. **Explain:** Explain why frozen does not deeply freeze a list field.
3. **Modify:** Add validation in post-init without duplicating the generated initializer.
4. **Debug:** Replace a shared mutable field default with a factory.

<details>
<summary>Hints</summary>

Field annotations describe intent; the post-init method enforces the runtime value contract.

</details>

## Independent task: dataclasses & value objects

In `Practice/06_Dataclasses_And_Value_Objects.py`, complete this task:

Define a frozen dataclass Expense with category:str and amount:int. In post-init reject a blank category or an amount whose type is not exactly int or is negative, using ValueError. Construct food/120 and print its fields as one line. Attempt food/True and print `Rejected` for ValueError.

Expected output:

```text
food 120
Rejected
```
