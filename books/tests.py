from rest_framework.test import APITestCase
from .models import Book

class BookTests(APITestCase):
    def test_get_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)

