from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .recommendation import recommend_books, fetch_books_from_google, parse_book_data
import logging


logger = logging.getLogger(__name__)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['GET'])
def recommend_books_view(request):
    user_id = request.GET.get('user_id')

    if not user_id:
        return render(request, 'error.html', {'error': 'User ID is required'})

    try:
        recommended_books = recommend_books(user_id=user_id)    
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)}) 

    return render(request, 'recommendations.html', {'recommended_books': recommended_books})

@api_view(['GET'])
def search_books_view(request):
    query = request.GET.get('query', '')
    if not query:
        return render(request, 'search_results.html', {'books': [], 'query': query})
    
    items = fetch_books_from_google(query)
    books_data = parse_book_data(items)
    # Render the search results template with the book data
    return render(request, 'search_results.html', {'books': books_data, 'query': query})

@api_view(['GET'])
def home_view(request):
    # Fetch featured books here (assuming you have a method to get them)
    featured_books = Book.objects.filter(is_featured=True)
    return render(request, 'home.html', {'featured_books': featured_books})

@api_view(['GET'])
def book_detail_view(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'book_detail.html', {'book': book})

@api_view(['GET'])
def search_results_view(request):
    query = request.GET.get('query', '')
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'books': books, 'query': query})

