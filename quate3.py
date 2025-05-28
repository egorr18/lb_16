import json
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
        return self.return_date and self.return_date > self.due_date

    def reading_time_days(self):
        if self.return_date:
            delta = self.return_date - self.issue_date
            return delta.days + delta.seconds / 86400
        return None

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

    def calculate_popularity(self):
        """Підрахунок кількості видач кожної книги"""
        popularity = {}
        for loan in self.loans:
            title = loan.book.title
            popularity[title] = popularity.get(title, 0) + 1
        return popularity

    def calculate_return_rate(self):
        """Відсоток повернення книг"""
        total_loans = len(self.loans)
        if total_loans == 0:
            return 0.0
        returned = sum(1 for loan in self.loans if loan.return_date is not None)
        return (returned / total_loans) * 100

    def calculate_avg_reading_time(self):
        """Середній час читання в днях серед повернених книг"""
        reading_times = [loan.reading_time_days() for loan in self.loans if loan.return_date]
        if not reading_times:
            return 0.0
        return sum(reading_times) / len(reading_times)

    def export_statistics_json(self, filename="library_stats.json"):
        stats = {
            "popularity": self.calculate_popularity(),
            "return_rate_percent": round(self.calculate_return_rate(), 2),
            "average_reading_time_days": round(self.calculate_avg_reading_time(), 2)
        }
        with open(filename, 'w') as f:
            json.dump(stats, f, indent=4)
        print(f"Statistics exported to {filename}")

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

    for loan in library.loans:
        if loan.book.title == "1984":
            loan.issue_date -= timedelta(days=10)
            loan.due_date -= timedelta(days=3)

    library.return_book("1984", reader1)
    library.return_book("Harry Potter", reader2)

    print("\n--- Statistics ---")
    print("Popularity:", library.calculate_popularity())
    print("Return rate (%):", library.calculate_return_rate())
    print("Average reading time (days):", library.calculate_avg_reading_time())

    library.export_statistics_json()
