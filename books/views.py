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
        return Response({'error': 'User ID is required'}, status=400)

    try:
        recommended_books = recommend_books(user_id=user_id)    
    except Exception as e:
        return Response({'error': str(e)}, status=500) 

    serializer = BookSerializer(recommended_books, many=True)
    return Response({'recommended_books': serializer.data}, status=200)

@api_view(['GET'])
def search_books_view(request):
    query = request.GET.get('query', '')
    if not query:
        return Response({'books': [], 'query': query}, status=200)
    
    items = fetch_books_from_google(query)
    books_data = parse_book_data(items)
    return Response({'books': books_data, 'query': query}, status=200)

@api_view(['GET'])
def home_view(request):
    featured_books = Book.objects.filter(is_featured=True)
    serializer = BookSerializer(featured_books, many=True)
    return Response({'featured_books': serializer.data}, status=200)

@api_view(['GET'])
def book_detail_view(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'error': "Book does not exist"}, status=404)
    
    serializer = BookSerializer(book)
    return Response({'book': serializer.data}, status=200)

@api_view(['GET'])
def search_results_view(request):
    query = request.GET.get('query', '')
    books = Book.objects.filter(title__icontains=query)
    serializer = BookSerializer(books, many=True)
    return Response({'books': serializer.data, 'query': query}, status=200)

