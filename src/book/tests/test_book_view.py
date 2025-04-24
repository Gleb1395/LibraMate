from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Book
from book.serializers import BookSerializer

BOOK_URL = reverse("book:books-list")


class BookListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self._create_book()

    def _create_book(self):
        self.book_1 = Book.objects.create(
            title="The Python Prophecy",
            author="Ada Lennox",
            cover=Book.Cover.HARD,
            inventory=50,
            daily_fee=10,
        )
        self.book_2 = Book.objects.create(
            title="Django Unleashed",
            author="Carl Rutherford",
            cover=Book.Cover.HARD,
            inventory=50,
            daily_fee=10,
        )
        self.book_3 = Book.objects.create(
            title="RESTful Tales",
            author="Nina Kovacs",
            cover=Book.Cover.HARD,
            inventory=50,
            daily_fee=10,
        )
        self.book_4 = Book.objects.create(
            title="The ORM Enigma",
            author="Victor Blaine",
            cover=Book.Cover.HARD,
            inventory=50,
            daily_fee=10,
        )

    def test_books_list_success(self):
        """
        Test for successful retrieval of the books list.
        """
        response = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_books_filter_by_title(self):
        """
        A tests of filtering books by title.
        """
        response = self.client.get(
            BOOK_URL,
            {
                "title": "The Python Prophecy",
            },
        )

        book_filter = Book.objects.filter(title__icontains="The Python Prophecy")
        serializer = BookSerializer(book_filter, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_books_filter_by_author(self):
        """
        A tests of filtering books by author.
        """
        response = self.client.get(
            BOOK_URL,
            {
                "author": "Victor Blaine",
            },
        )

        book_filter = Book.objects.filter(author__icontains="Victor Blaine")
        serializer = BookSerializer(book_filter, many=True)

        self.assertEqual(response.data, serializer.data)
