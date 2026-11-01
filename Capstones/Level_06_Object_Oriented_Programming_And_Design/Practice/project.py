# Independent task: Library catalog and borrowing model
#
# Define frozen Book(book_id, title) with nonblank string fields. Define
# MemoryCatalog.add(book), rejecting duplicate IDs with ValueError, and get(book_id), raising
# KeyError when absent. Add ids() returning a new alphabetical list of catalog IDs for the
# composed Library to use.
#
# Define Library(catalog=None) with register(book), borrow(book_id, member),
# return_book(book_id), and available_ids(). A successful borrow records the loan and returns
# the Book. Reject blank members and already-borrowed books before changing state. Missing
# catalog IDs raise KeyError; returning a book with no active loan raises ValueError.
# available_ids returns an alphabetical independent list.
#
# Demonstrate registering PY1/Python Basics, borrowing it for Mika, rejecting a second borrow,
# returning it, and showing that a newly constructed second library has no books.
#
# Expected output:
#
# Borrowed: Python Basics
# Second borrow rejected
# Available: ['PY1']
# Other library books: 0

