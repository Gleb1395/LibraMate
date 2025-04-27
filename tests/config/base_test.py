from tests.services.book.api_books import BooksAPI
from tests.services.users.api_users import UsersAPI


class BaseTest:

    def setup_method(self):
        self.api_users = UsersAPI()
        self.api_books = BooksAPI()
