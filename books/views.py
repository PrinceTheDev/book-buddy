from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .recommendation import recommend_books, fetch_books_from_google, parse_book_data
from .serializers import BookSerializer
from .models import Book
from django.template.loader import render_to_string

# Django Views
def home_view(request):
    return render(request, 'home.html')

def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book})

def search_results_view(request):
    query = request.GET.get('query', '')
    if not query:
        return render(request, 'search_results.html', {'error': 'Query parameter is required'})
    
    items = fetch_books_from_google(query)
    books = parse_book_data(items)
    return render(request, 'search_results.html', {'books': books, 'query': query})

@api_view(['GET'])
def recommendations_view(request):
    user_id = request.query_params.get('user_id', None)
    recommended_books = recommend_books(user_id)
    serializer = BookSerializer(recommended_books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_books_view(request):
    query = request.query_params.get('query', '')
    if not query:
        return Response({'error': 'Query parameter is required'}, status=400)
    
    items = fetch_books_from_google(query)
    books = parse_book_data(items)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

