from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, recommendations_view, search_books_view, home_view, book_detail_view, search_results_view

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('books/<int:book_id>/', book_detail_view, name='book_detail'),
    path('search/', search_results_view, name='search_results'),
    path('recommendations/', recommendations_view, name='recommendations'),
    path('search-books/', search_books_view, name='search_books'),
    path('api/', include(router.urls)),
]

