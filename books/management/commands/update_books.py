from django.core.management.base import BaseCommand
from books.recommendation import update_books_from_google
from books.models import User, Book, UserBookInteraction
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Update books from Google Books API and populate users and interactions'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='Search query for Google Books API')

    def handle(self, *args, **kwargs):
        query = kwargs['query']
        self.stdout.write(f'Updating books with query: {query}')
        
        # Update books from Google Books API
        update_books_from_google(query)
        self.stdout.write('Books updated successfully')

        # Populate users and interactions
        self.stdout.write('Populating users and interactions...')
        self.populate_users_and_interactions()
        self.stdout.write('Users and interactions populated successfully')

    def populate_users_and_interactions(self):
        # Create 50 users
        for i in range(1, 51):
            User.objects.create(
                username=f'user{i}',
                email=f'user{i}@example.com'
            )

        # Sample books (use existing books or create new ones)
        sample_books = Book.objects.all()
        
        if not sample_books:
            sample_books = [
                {'isbn': '9780439139601', 'title': 'Harry Potter and the Goblet of Fire', 'author': 'J.K. Rowling', 'publication_date': '2000-07-08', 'genre': 'Fantasy'},
                {'isbn': '9780061120084', 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'publication_date': '1960-07-11', 'genre': 'Fiction'},
                {'isbn': '9780451524935', 'title': '1984', 'author': 'George Orwell', 'publication_date': '1949-06-08', 'genre': 'Dystopian'},
                {'isbn': '9780307588364', 'title': 'The Girl with the Dragon Tattoo', 'author': 'Stieg Larsson', 'publication_date': '2005-08-01', 'genre': 'Thriller'},
                {'isbn': '9781451673319', 'title': 'Fahrenheit 451', 'author': 'Ray Bradbury', 'publication_date': '1953-10-19', 'genre': 'Science Fiction'},
            ]

            for book in sample_books:
                Book.objects.create(
                    isbn=book['isbn'],
                    title=book['title'],
                    author=book['author'],
                    publication_date=book.get('publication_date', None),
                    genre=book.get('genre', ''),
                    description=book.get('description', ''),
                    cover_image=book.get('cover_image', '')
                )

        # Create sample interactions
        for user in User.objects.all():
            for book in Book.objects.all():
                UserBookInteraction.objects.create(
                    user=user,
                    book=book,
                    interaction_type=random.choice(['view', 'like', 'rate', 'review']),
                    timestamp=self.random_date()
                )

    def random_date(self, start_year=2000, end_year=2024):
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        delta = end_date - start_date
        random_days = random.randrange(delta.days)
        return start_date + timedelta(days=random_days)
