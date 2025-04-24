from django.contrib.auth import get_user_model
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


class BookPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = BOOK_URL
        self._create_book()
        self.user = get_user_model().objects.create_user(
            email="user@user.com",
            password="user",
            username="user",
            phone="+380888888811",
        )
        self.admin = get_user_model().objects.create_superuser(
            password="admin",
            email="admin@admin.com",
        )

    def _create_book(self):
        self.book = Book.objects.create(
            title="The Python Prophecy",
            author="Ada Lennox",
            cover=Book.Cover.HARD,
            inventory=50,
            daily_fee=10,
        )

    def test_list_books_anonymous_allowed(self):
        """
        Ensure that an anonymous (unauthenticated) user
        can access the list of books.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_book_anonymous_forbidden(self):
        """
        Ensure that an anonymous user cannot retrieve
        details of a specific book and receives a 401 response.
        """
        url = reverse("book:books-detail", args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_book_authenticated_allowed(self):
        """
        Ensure that an authenticated user can successfully
        retrieve the details of a specific book.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("book:books-detail", args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_not_admin_forbidden(self):
        """
        Ensure that an authenticated non-admin user
        is not allowed to create a new book entry.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url,
            {
                "title": "New Book",
                "author": "Someone",
                "cover": Book.Cover.SOFT,
                "inventory": 10,
                "daily_fee": 5,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_admin_allowed(self):
        """
        Ensure that an admin user is allowed to create
        a new book entry successfully.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            self.url,
            {
                "title": "New Admin Book",
                "author": "Admin Author",
                "cover": Book.Cover.SOFT,
                "inventory": 10,
                "daily_fee": 5,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
