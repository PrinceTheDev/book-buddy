from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField(blank=True, null=True, default=None)
    genre = models.CharField(max_length=255)
    description = models.TextField(default='No description available')
    cover_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

