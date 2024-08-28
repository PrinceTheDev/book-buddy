from django.urls import path, include
from .views import BookViewSet, recommendations_view, search_books_view, home_view, book_detail_view, search_results_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('book/<int:book_id>/', book_detail_view, name='book_detail'),
    path('search/', search_results_view, name='search_results'),
    path('api/', include(router.urls)),
    path('api/recommendations/', recommendations_view, name='recommendations'),
    path('api/search-books/', search_books_view, name='search_books'),
]

