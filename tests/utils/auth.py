import requests

HOST = "http://127.0.0.1:8000/api/v1/"


def login(email: str, password: str) -> dict:
    response = requests.post(
        f"{HOST}user/users/token/",
        json={"email": email, "password": password},
    )
    response.raise_for_status()
    data = response.json()
    return data
