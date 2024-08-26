from import_export import resources
from .models import Book, User, Rating

class BookResource(resources.ModelResource):
    class Meta:
        model = Book

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class RatingResource(resources.ModelResource):
    class Meta:
        model = Rating
