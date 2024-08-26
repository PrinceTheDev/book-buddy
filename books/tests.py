from django.test import TestCase, Client
from django.urls import reverse
from .models import Book, User, Rating

class BookTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.book = Book.objects.create(
            isbn='1234567890',
            title='Test Book',
            author='Test Author',
            year_of_publication=2024,
            publisher='Test Publisher',
            image_url_s='http://example.com/small.jpg',
            image_url_m='http://example.com/medium.jpg',
            image_url_l='http://example.com/large.jpg'
        )
        Rating.objects.create(user=self.user, book=self.book, book_rating=5)

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Book Buddy')

    def test_book_list_page(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    def test_book_detail_page(self):
        response = self.client.get(reverse('book_detail', args=['1234567890']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Author')

    def test_recommendation_page(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('recommend'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recommended Books for You')

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Should redirect after login

    def test_signup(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after signup

    def test_profile_page(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Profile')
