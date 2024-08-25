"""
This model consists of models for the books, users and ratings. 
Gotten from the data set, it will be used to help in the recommendation algorithm.
"""

from django.db import models


class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year_of_publication = models.IntegerField()
    publisher = models.CharField(max_length=255)
    image_url_s = models.URLField()
    image_url_m = models.URLField()
    image_url_l = models.URLField()

    def __str__(self):
        return self.title

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"User {self.user_id}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user} rated {self.book} with a score of {self.rating}"
