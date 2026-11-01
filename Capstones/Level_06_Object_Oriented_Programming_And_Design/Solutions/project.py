from dataclasses import dataclass

@dataclass(frozen=True)
class Book:
    book_id: str
    title: str

    def __post_init__(self):
        if not isinstance(self.book_id, str) or not self.book_id.strip():
            raise ValueError("Invalid book ID")
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Invalid title")

class MemoryCatalog:
    def __init__(self):
        self._books = {}

    def add(self, book):
        if book.book_id in self._books:
            raise ValueError("Duplicate book")
        self._books[book.book_id] = book

    def get(self, book_id):
        return self._books[book_id]

    def ids(self):
        return sorted(self._books)

class Library:
    def __init__(self, catalog=None):
        if catalog is None:
            catalog = MemoryCatalog()
        self._catalog = catalog
        self._loans = {}

    def register(self, book):
        self._catalog.add(book)

    def borrow(self, book_id, member):
        book = self._catalog.get(book_id)
        if not isinstance(member, str) or not member.strip():
            raise ValueError("Invalid member")
        if book_id in self._loans:
            raise ValueError("Already borrowed")
        self._loans[book_id] = member.strip()
        return book

    def return_book(self, book_id):
        self._catalog.get(book_id)
        if book_id not in self._loans:
            raise ValueError("No active loan")
        del self._loans[book_id]

    def available_ids(self):
        result = []
        for book_id in self._catalog.ids():
            if book_id not in self._loans:
                result.append(book_id)
        return result

if __name__ == "__main__":
    library = Library()
    library.register(Book("PY1", "Python Basics"))
    print(f"Borrowed: {library.borrow('PY1', 'Mika').title}")
    try:
        library.borrow("PY1", "José")
    except ValueError:
        print("Second borrow rejected")
    library.return_book("PY1")
    print(f"Available: {library.available_ids()}")
    print(f"Other library books: {len(Library().available_ids())}")
