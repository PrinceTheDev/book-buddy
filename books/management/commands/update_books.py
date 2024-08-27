from django.core.management.base import BaseCommand
from books.recommendation import update_books_from_google

class Command(BaseCommand):
    help = 'Update books from Google Books API'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='Search query for Google Books API')

    def handle(self, *args, **kwargs):
        query = kwargs['query']
        self.stdout.write(f'Updating books with query: {query}')
        update_books_from_google(query)
        self.stdout.write('Books updated successfully')

