from django.db import models
from django.contrib.auth.models import AbstractUser

class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=255)
    year_of_publication = models.IntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=255)
    image_url_s = models.URLField(max_length=1024, null=True, blank=True)
    image_url_m = models.URLField(max_length=1024, null=True, blank=True)
    image_url_l = models.URLField(max_length=1024, null=True, blank=True)
    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    location = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user} rated {self.book} with a score of {self.rating}"
