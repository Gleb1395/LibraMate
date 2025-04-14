from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    cover = serializers.ChoiceField(choices=Book.Cover.choices, default=Book.Cover.HARD)

    class Meta:
        model = Book
        fields = ("title", "author", "cover", "inventory", "daily_fee")
