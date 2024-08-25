"""
This modeule contains specific functions that will be used to load the database gotten from the sample dataset folder, into the books app
"""

import os
import csv
import django
from books.model import Book, User, Rating


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_buddy.settings')
django.setup()


def load_books(file_path='dataset/BX-books.csv'):
    """loads the databse for the books"""
    with open(file_path, 'r', encoding='utf-8') as file:
        reader= csv.DictReader(file, dlimeter=';')
        for row in reader:
            Book.objects.get_or_create(
                isbn=row['ISBN'],
                defaults={
                    'title': row['Book-Title'],
                    'author': row['Book-Author'],
                    'year_of_publication': int(row['Year-Of-Publication']),
                    'publisher': row['Publisher'],
                    'image_url_s': row['Image-URL-S'],
                    'image_url_m': row['Image-URL-M'],
                    'image_url_l': row['Image-URL-L'],
                }
            )

def load_users(file_path='dataset/BX-users.csv'):
    """loads the daabase for users"""
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            User.objects.get_or_create(
                user_id=int(row['User-ID']),
                defaults={
                    'location': row['Location'],
                    'age': int(row['Age']) if row['Age'] != 'NULL' else None,
                }
            )

def load_ratings(file_path='datset/BX-ratings.csv'):
    """This functio loads the database for the books ratings"""
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            user = User.objects.get(user_id=int(row['User-ID']))
            book = Book.objects.get(isbn=row['ISBN'])
            Rating.objects.get_or_create(
                user=user,
                book=book,
                defaults={'rating': int(row['Book-Rating'])}
            )


if __name_=='__main__':
    load_books()
    load_users()
    load_ratings()
