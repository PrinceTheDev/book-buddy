from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField(blank=True, null=True)
    genre = models.CharField(max_length=255)
    description = models.TextField(default='No description available')
    cover_image = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class UserBookInteraction(models.Model):
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('like', 'Like'),
        ('rate', 'Rate'),
        ('review', 'Review'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.book.title}"

