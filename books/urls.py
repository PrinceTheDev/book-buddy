from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('books/', views.book_list, name='book_list'),
    path('books/<str:isbn>/', views.book_detail, name='book_detail'),
    path('recommend/', views.recommend_books, name='recommend'),
    path('contact/', views.contact, name='contact'),
]
