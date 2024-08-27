from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .recommendation import recommend_books

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['GET'])
def recommendations_view(request):
    user_id = request.query_params.get('user_id', None)
    recommended_books = recommend_books(user_id)
    serializer = BookSerializer(recommended_books, many=True)
    return Response(serializer.data)

