HOST = "http://127.0.0.1:8000/api/v1/user"


class Endpoints:

    create_user = f"{HOST}/users/"
    get_user_by_id = lambda self, id: f"{HOST}/users/me/{id}/"
