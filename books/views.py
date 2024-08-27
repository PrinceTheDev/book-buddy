from rest_framework.decorators import api_view
from rest_framework.response import Response
from .recommendation import recommend_books, fetch_books_from_google, parse_book_data
from .serializers import BookSerializer
from rest_framework import viewsets
from .models import Book


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

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

