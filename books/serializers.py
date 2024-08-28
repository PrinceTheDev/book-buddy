from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField()
    id = serializers.CharField()
    class Meta:
        model = Book
        fields = '__all__'

