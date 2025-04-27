HOST = "http://127.0.0.1:8000/api/v1/book"


class BookEndpoint:
    list_books = f"{HOST}/books/"
    get_book_by_id = lambda self, id: f"{HOST}/books/{id}/"
    create_book = f"{HOST}/books/"
