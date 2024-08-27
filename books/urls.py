from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, recommendations_view, search_books_view

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recommendations/', recommendations_view),
    path('search-books/', search_books_view),
]

