from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book, CustomUser, Rating
from .forms import ContactForm, CustomUserCreationForm
import requests
from .recommendation import get_recommendations
from django.conf import settings


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    user_ratings = Rating.objects.filter(user=request.user)
    return render(request, 'profile.html', {'ratings': user_ratings})

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_detail(request, isbn):
    book = Book.objects.get(isbn=isbn)
    return render(request, 'book_detail.html', {'book': book})

@login_required
def recommend_books(request):
    user = request.user
    recommendations = get_recommendations(user.id)
    return render(request, 'recommend.html', {'recommended_books': recommendations})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Contact Form Submission'
            message = f"Name: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\nMessage: {form.cleaned_data['message']}"
            recipient_list = ['prince.uchendu07@gmail.com']
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def fetch_books_from_google_api(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={settings.GOOGLE_BOOKS_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

def update_books_from_google(request):
    query = 'programming'
    books_data = fetch_books_from_google_api(query)
    for item in books_data:
        volume_info = item['volumeInfo']
        Book.objects.update_or_create(
            isbn=volume_info.get('industryIdentifiers', [{}])[0].get('identifier', ''),
            defaults={
                'title': volume_info.get('title', ''),
                'author': ', '.join(volume_info.get('authors', [])),
                'year_of_publication': volume_info.get('publishedDate', '').split('-')[0],
                'publisher': volume_info.get('publisher', ''),
                'image_url_m': volume_info.get('imageLinks', {}).get('medium', ''),
            }
        )
    return redirect('book_list')
