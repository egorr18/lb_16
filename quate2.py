from datetime import datetime, timedelta

class Reader:
    def __init__(self, name):
        self.name = name

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def __str__(self):
        return f"'{self.title}' by {self.author}"

class LoanRecord:
    def __init__(self, book, reader, due_date):
        self.book = book
        self.reader = reader
        self.issue_date = datetime.now()
        self.due_date = due_date
        self.return_date = None

    def mark_returned(self):
        self.return_date = datetime.now()

    def is_overdue(self):
        return datetime.now() > self.due_date

class Library:
    def __init__(self):
        self.books = []
        self.loans = []

    def add_book(self, book: Book):
        self.books.append(book)

    def issue_book(self, title, reader: Reader, days=14):
        for book in self.books:
            if book.title == title and book.available:
                book.available = False
                due_date = datetime.now() + timedelta(days=days)
                loan = LoanRecord(book, reader, due_date)
                self.loans.append(loan)
                print(f"Book '{book.title}' issued to {reader.name} until {due_date.date()}")
                return
        print(f"Book '{title}' is not available.")

    def return_book(self, title, reader: Reader):
        for loan in self.loans:
            if loan.book.title == title and loan.reader.name == reader.name and loan.return_date is None:
                loan.mark_returned()
                loan.book.available = True
                status = "LATE" if loan.is_overdue() else "on time"
                print(f"Book '{title}' returned by {reader.name} ({status}).")
                return
        print(f"No active loan found for '{title}' by {reader.name}.")

    def show_loans(self):
        print("\nLoan History:")
        for loan in self.loans:
            status = "Returned" if loan.return_date else "Borrowed"
            print(f"{loan.book.title} - {loan.reader.name} ({status})")

if __name__ == "__main__":
    library = Library()

    book1 = Book("1984", "George Orwell")
    book2 = Book("Harry Potter", "J.K. Rowling")
    reader1 = Reader("Alice")
    reader2 = Reader("Bob")

    library.add_book(book1)
    library.add_book(book2)

    library.issue_book("1984", reader1)
    library.issue_book("Harry Potter", reader2, days=7)

    library.return_book("1984", reader1)

    library.return_book("1984", reader1)

    library.show_loans()
