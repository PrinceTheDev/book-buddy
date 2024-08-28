from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .recommendation import recommend_books, fetch_books_from_google, parse_book_data
from .serializers import BookSerializer
from .models import Book
from django.template.loader import render_to_string
from rest_framework import viewsets


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializers_class = BookSerializer

def home_view(request):
    featured_books = Book.objects.all().order_by('-publication_date')[:5]
    return render(request, 'home.html', {'featured_books': featured_books})

def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    related_books = Book.objects.exclude(id=book_id).order_by('-publication_date')[:5]
    return render(request, 'book_detail.html', {'book': book, 'related_books': related_books})

def search_results_view(request):
    query = request.GET.get('query', '')
    if not query:
        return render(request, 'search_results.html', {'error': 'Query parameter is required'})
    
    items = fetch_books_from_google(query)
    books = parse_book_data(items)
    return render(request, 'search_results.html', {'search_results': books, 'query': query})

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

def recommend_books_view(request):
    user_id = request.GET.get('user_id')
    
    if not user_id:
        return render(request, 'error.html', {'error': 'User ID is required'})
    
    try:
        recommended_books = recommend_books(user_id=user_id)
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})

    return render(request, 'recommendations.html', {'recommended_books': recommended_books})
