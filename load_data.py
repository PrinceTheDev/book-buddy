"""
This modeule contains specific functions that will be used to load the database gotten from the sample dataset folder, into the books app
"""

import os
import csv
import django
from tqdm import tqdm


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_buddy.settings')
django.setup()

from books.models import Book, User, Rating


def load_books(file_path='dataset/books.csv'):
    """loads the databse for the books"""
    books = []
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        reader= csv.DictReader(file, delimiter=';')
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
    Book.objects.bulk_create(books, batch_size=1000)


def load_users(file_path='dataset/users.csv'):
    """loads the daabase for users"""
    users = []
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            user_id = int(row['User-ID'])
            if not User.objects.filter(user_id=user_id).exists():
                users.append(User(
                    user_id=int(row['User-ID']),
                    location=row['Location'],
                    age=int(row['Age']) if row['Age'] != 'NULL' else None,
            ))
    User.objects.bulk_create(users, batch_size=1000)


def load_ratings(file_path='dataset/ratings.csv'):
    """This functio loads the database for the books ratings"""
    ratings = []
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            try:
                user = User.objects.get(user_id=int(row['User-ID']))
                book = Book.objects.get(isbn=row['ISBN'])
                ratings.append(Rating(
                    user=user,
                    book=book,
                    rating=int(row['Book-Rating'])
            ))
            except Book.DoesNotExist:
                print(f"Book with ISBN {row['ISBN']} does not exist. Skipping rating.")
    if ratings:
        Rating.objects.bulk_create(ratings, batch_size=1000)


if __name__=='__main__':
    load_books()
    load_users()
    load_ratings()
