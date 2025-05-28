class Author:
    def __init__(self, name):
        self.name = name

class Book:
    def __init__(self, title, author: Author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"'{self.title}' by {self.author.name}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book: Book):
        self.books.append(book)
        print(f"Added: {book}")

    def remove_book(self, title: str):
        for book in self.books:
            if book.title == title:
                self.books.remove(book)
                print(f"Removed: {book}")
                return
        print(f"Book '{title}' not found in library.")

    def find_book(self, keyword: str):
        results = [book for book in self.books if keyword.lower() in book.title.lower()]
        if results:
            print("Search results:")
            for book in results:
                print(f"- {book}")
        else:
            print(f"No books found matching '{keyword}'.")

if __name__ == "__main__":
    author1 = Author("George Orwell")
    author2 = Author("J.K. Rowling")

    book1 = Book("1984", author1)
    book2 = Book("Harry Potter and the Philosopher's Stone", author2)

    library = Library()
    library.add_book(book1)
    library.add_book(book2)

    library.find_book("Harry")
    library.remove_book("1984")
    library.find_book("1984")
