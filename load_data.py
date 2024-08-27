"""
This module contains functions to load data from CSV files into the Django models for the books app.
"""

import os
import csv
import django
from books.models import Book, User, Rating

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_buddy.settings')
django.setup()

def load_books(file_path='dataset/books.csv'):
    """Load books into the database from a CSV file."""
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    books = []
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        reader = csv.DictReader(file, delimiter=';')  # Update delimiter if necessary
        for row in reader:
            try:
                year_of_publication = int(row['Year-Of-Publication'])
            except ValueError:
                year_of_publication = None

            if not Book.objects.filter(isbn=row['ISBN']).exists():
                books.append(Book(
                    isbn=row['ISBN'],
                    title=row['Book-Title'],
                    author=row['Book-Author'],
                    year_of_publication=year_of_publication,
                    publisher=row['Publisher'],
                    image_url_s=row['Image-URL-S'],
                    image_url_m=row['Image-URL-M'],
                    image_url_l=row['Image-URL-L'],
                ))

    if books:
        Book.objects.bulk_create(books, batch_size=1000)
        print(f"Loaded {len(books)} books.")
    else:
        print("No new books to load.")

def load_users(file_path='dataset/users.csv'):
    """Load users into the database from a CSV file."""
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    users = []
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        reader = csv.DictReader(file, delimiter=';')  # Update delimiter if necessary
        for row in reader:
            user_id = int(row['User-ID'])
            if not User.objects.filter(user_id=user_id).exists():
                users.append(User(
                    user_id=user_id,
                    location=row['Location'],
                    age=int(row['Age']) if row['Age'] != 'NULL' else None,
                ))

    if users:
        User.objects.bulk_create(users, batch_size=1000)
        print(f"Loaded {len(users)} users.")
    else:
        print("No new users to load.")

def load_ratings(file_path='dataset/ratings.csv'):
    """Load book ratings into the database from a CSV file."""
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    ratings = []
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        reader = csv.DictReader(file, delimiter=';')  # Update delimiter if necessary
        for row in reader:
            try:
                user = User.objects.get(user_id=int(row['User-ID']))
                book = Book.objects.get(isbn=row['ISBN'])
                ratings.append(Rating(
                    user=user,
                    book=book,
                    rating=int(row['Book-Rating']),
                ))
            except Book.DoesNotExist:
                print(f"Book with ISBN {row['ISBN']} does not exist. Skipping rating.")
            except User.DoesNotExist:
                print(f"User with ID {row['User-ID']} does not exist. Skipping rating.")

    if ratings:
        Rating.objects.bulk_create(ratings, batch_size=1000)
        print(f"Loaded {len(ratings)} ratings.")
    else:
        print("No new ratings to load.")

if __name__ == '__main__':
    load_books()
    load_users()
    load_ratings()

