from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from .models import Book, User, Rating
from .resources import BookResource, UserResource, RatingResource

@admin.register(Book)
class BookAdmin(ExportActionModelAdmin):
    resource_class = BookResource

@admin.register(User)
class UserAdmin(ExportActionModelAdmin):
    resource_class = UserResource

@admin.register(Rating)
class RatingAdmin(ExportActionModelAdmin):
    resource_class = RatingResource

