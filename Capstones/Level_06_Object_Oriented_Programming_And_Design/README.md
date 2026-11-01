# Level 6 capstone: Library catalog and borrowing model

**Prerequisites:** [all lessons in Level 6](../../Courses/Level_06_Object_Oriented_Programming_And_Design/README.md). **Submission:** `Practice/project.py`.

Build a small object model with clear ownership. Book is an immutable value record. MemoryCatalog owns books by unique ID. Library composes a catalog and owns its own active loans. This separation lets the borrowing rules remain independent of how catalog data is eventually stored.

A failed borrow must not modify the loan table. Returning available IDs should not expose an internal mutable dictionary. Each independently constructed Library receives a fresh default catalog and loan collection. Shared state should occur only when an explicit collaborator is passed.

The reference is in memory and has no authentication, persistence, or real-world lending policy. Its purpose is to demonstrate state transitions, composition, instance isolation, and justified value objects.

## Project task

Define frozen Book(book_id, title) with nonblank string fields. Define MemoryCatalog.add(book), rejecting duplicate IDs with ValueError, and get(book_id), raising KeyError when absent. Add ids() returning a new alphabetical list of catalog IDs for the composed Library to use.

Define Library(catalog=None) with register(book), borrow(book_id, member), return_book(book_id), and available_ids(). A successful borrow records the loan and returns the Book. Reject blank members and already-borrowed books before changing state. Missing catalog IDs raise KeyError; returning a book with no active loan raises ValueError. available_ids returns an alphabetical independent list.

Demonstrate registering PY1/Python Basics, borrowing it for Mika, rejecting a second borrow, returning it, and showing that a newly constructed second library has no books.

Expected output:

```text
Borrowed: Python Basics
Second borrow rejected
Available: ['PY1']
Other library books: 0
```
