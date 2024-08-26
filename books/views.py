from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import ContactForm
from .recommendation import get_recommendations

# Home page view
def home(request):
    return render(request, 'home.html')

# Signup page view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login page view
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

# Logout view
def user_logout(request):
    logout(request)
    return redirect('home')

# Profile page view
@login_required
def profile(request):
    return render(request, 'profile.html')

# Book list page view
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

# Book detail page view
def book_detail(request, isbn):
    book = Book.objects.get(isbn=isbn)
    return render(request, 'book_detail.html', {'book': book})

# Recommendations page view
@login_required
def recommend_books(request):
    user = request.user
    recommendations = get_recommendations(user)
    return render(request, 'recommend.html', {'recommendations': recommendations})

# Contact page view
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

