import allure
import requests
from django.contrib.auth import get_user_model

from tests.config.headers import Headers
from tests.services.users.endpoints import Endpoints
from tests.services.users.models.user_model import UserModel
from tests.services.users.payloads import Payloads
from tests.utils.helper import Helper


class UsersAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Create user")
    def create_user(self):
        response = requests.post(
            url=self.endpoints.create_user,
            headers=self.headers.admin(),
            json=self.payloads.create_user,
        )
        assert response.status_code == 201, response.json()
        self.attach_response(response.json())
        data = response.json()
        data.pop("access", None)
        data.pop("refresh", None)
        model = UserModel(**data)  # NOQA E402
        user = get_user_model().objects.create(**data)
        return user

    @allure.step("Get users by ID")
    def get_user_by_id(self, id):
        response = requests.get(
            url=self.endpoints.get_user_by_id(id),
            headers=self.headers.admin(),
        )
        assert response.status_code == 200, response.json()
        self.attach_response(response.json())
        data = response.json()
        model = get_user_model().objects.get(email=data["email"])
        return model
