import allure
import pytest

from tests.config.base_test import BaseTest


@allure.epic("Book Management")
@allure.feature("Books")
class TestBooks(BaseTest):

    @pytest.mark.books
    @allure.title("Get list of books")
    def test_get_list_books(self):
        self.api_books.get_list_books_anonymous_allowed()

    @pytest.mark.books
    @allure.title("Anonymous user cannot retrieve book by ID")
    def test_anonymous_user_cannot_retrieve_book_by_id(self):
        books = self.api_books.get_list_books_anonymous_allowed()
        first_book = books[0]
        self.api_books.anonymous_retrieve_book_by_id(id=first_book.id)

    @pytest.mark.books
    @allure.title("Regular user retrieve book by ID")
    def test_regular_user_retrieve_book_by_id(self):
        books = self.api_books.get_list_books_anonymous_allowed()
        first_book = books[0]
        self.api_books.anonymous_retrieve_book_by_id(id=first_book.id)

    @pytest.mark.books
    @allure.title("Admin allowed create book")
    def test_admin_allowed_create_book_(self):
        self.api_books.admin_create_book()
