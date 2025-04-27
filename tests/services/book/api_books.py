import allure
import requests

from tests.services.book.endpoints import BookEndpoint
from tests.services.book.models.book_model import BookModel
from tests.services.book.payloads import BookPayloads
from tests.config.headers import Headers
from tests.utils.helper import Helper


class BooksAPI(Helper):
    def __init__(self):
        super().__init__()
        self.payloads = BookPayloads()
        self.endpoints = BookEndpoint()
        self.headers = Headers()

    @allure.step("Get list of books")
    def get_list_books_anonymous_allowed(self):
        response = requests.get(
            url=self.endpoints.list_books,
        )
        assert response.status_code == 200, response.json()
        data = response.json()
        return [BookModel(**book) for book in data]

    @allure.step("Retrieve books anonymous user")
    def anonymous_retrieve_book_by_id(self, id):
        response = requests.get(
            url=self.endpoints.get_book_by_id(id),
        )
        assert response.status_code == 401, response.json()

    @allure.step("Retrieve books a regular user")
    def user_retrieve_book_by_id(self, id):
        response = requests.get(
            url=self.endpoints.get_book_by_id(id), headers=self.headers.user()
        )
        assert response.status_code == 200, response.json()

    @allure.step("Regular user can not create a book")
    def admin_create_book(self):
        response = requests.post(
            url=self.endpoints.create_book,
            headers=self.headers.admin(),
            json=self.payloads.create_book(),
        )
        assert response.status_code == 201, response.json()
        data = response.json()
        BookModel(**data)
