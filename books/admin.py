from django.contrib import admin
from .models import Book, UserBookInteraction

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publication_date', 'genre', 'description', 'cover_image')
    search_fields = ('title', 'author', 'isbn', 'genre')

admin.site.register(Book, BookAdmin)
admin.site.register(UserBookInteraction)

