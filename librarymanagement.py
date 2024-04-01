from datetime import datetime, timedelta

class Library:
    def __init__(self):
        self.catalog = {}
        self.users = {}
        self.transactions = []

    def add_book(self, book_id, title, author, quantity):
        self.catalog[book_id] = {'title': title, 'author': author, 'quantity': quantity}

    def display_catalog(self):
        print("Current Catalog:")
        for book_id, details in self.catalog.items():
            print(f"ID: {book_id}, Title: {details['title']}, Author: {details['author']}, Available Quantity: {details['quantity']}")

    def register_user(self, user_id, name):
        self.users[user_id] = {'name': name, 'books_checked_out': [], 'fine': 0}

    def checkout_book(self, user_id, book_id, checkout_date):
        if user_id not in self.users:
            print("User not found. Please register first.")
            return False
        if book_id not in self.catalog:
            print("Book not found in catalog.")
            return False
        if len(self.users[user_id]['books_checked_out']) >= 3:
            print("You have already checked out the maximum number of books.")
            return False
        if self.catalog[book_id]['quantity'] <= 0:
            print("Sorry, the book is not available at the moment.")
            return False

        self.transactions.append({'user_id': user_id, 'book_id': book_id, 'checkout_date': checkout_date})
        self.users[user_id]['books_checked_out'].append(book_id)
        self.catalog[book_id]['quantity'] -= 1
        print("Book checked out successfully.")
        return True

    def return_book(self, user_id, book_id, return_date):
        if user_id not in self.users:
            print("User not found.")
            return False
        if book_id not in self.catalog:
            print("Book not found in catalog.")
            return False
        if book_id not in self.users[user_id]['books_checked_out']:
            print("You haven't checked out this book.")
            return False

        checkout_date = None
        for transaction in self.transactions:
            if transaction['user_id'] == user_id and transaction['book_id'] == book_id:
                checkout_date = transaction['checkout_date']
                self.transactions.remove(transaction)
                break

        if not checkout_date:
            print("Error retrieving checkout date.")
            return False

        self.users[user_id]['books_checked_out'].remove(book_id)
        self.catalog[book_id]['quantity'] += 1

        due_date = checkout_date + timedelta(days=14)
        if return_date > due_date:
            days_overdue = (return_date - due_date).days
            fine = days_overdue * 1
            self.users[user_id]['fine'] += fine
            print(f"Book returned successfully. Overdue fine: ${fine}")
        else:
            print("Book returned successfully.")
        return True

    def get_overdue_books(self, user_id):
        overdue_books = []
        total_fine = 0
        for transaction in self.transactions:
            if transaction['user_id'] == user_id:
                due_date = transaction['checkout_date'] + timedelta(days=14)
                if datetime.now() > due_date:
                    days_overdue = (datetime.now() - due_date).days
                    fine = days_overdue * 1
                    total_fine += fine
                    overdue_books.append((transaction['book_id'], fine))
        return overdue_books, total_fine

library = Library()
library.add_book('B1', 'Python Programming', 'John Doe', 5)
library.add_book('B2', 'Introduction to Data Science', 'Jane Smith', 3)
library.add_book('B3', 'Machine Learning Basics', 'Alice Johnson', 2)

library.display_catalog()

library.register_user('U1', 'Alice')
library.register_user('U2', 'Bob')

library.checkout_book('U1', 'B1', datetime.now())
library.checkout_book('U1', 'B2', datetime.now())

library.return_book('U1', 'B1', datetime.now() + timedelta(days=10))
library.return_book('U1', 'B2', datetime.now() + timedelta(days=20))

overdue_books, total_fine = library.get_overdue_books('U1')
print("Overdue Books for User U1:")
for book_id, fine in overdue_books:
    print(f"Book ID: {book_id}, Fine: ${fine}")
print("Total Fine:", total_fine)


