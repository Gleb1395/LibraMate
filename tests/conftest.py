from django.core.management import call_command

import os

import pytest


from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from typing import Any
from dotenv import load_dotenv

from tests.utils.auth import login

load_dotenv()


ADMIN_EMAIL = os.getenv("API_EMAIL_ADMIN")
ADMIN_PASSWORD = os.getenv("API_LOGIN_PASSWORD_ADMIN")
ADMIN_PHONE = os.getenv("API_LOGIN_PHONE_ADMIN")
ADMIN_USERNAME = os.getenv("API_LOGIN_USERNAME_ADMIN")

USER_EMAIL = os.getenv("API_EMAIL_USER")
USER_PASSWORD = os.getenv("API_LOGIN_PASSWORD_USER")
USER_PHONE = os.getenv("API_LOGIN_PHONE_USER")
USER_USERNAME = os.getenv("API_LOGIN_USERNAME_USER")


@pytest.fixture(autouse=True)
def init_environment(db, transactional_db):
    call_command("flush", interactive=False, verbosity=0)


def _get_or_create_user(
    email: str,
    password: str,
    db_blocker,
    phone: str,
    username: str,
    superuser: bool = False,
) -> User:
    """
    Creates or gets a user with the given email from the database.
    If superuser=True - uses create_superuser(), otherwise create_user().
    Works inside django_db_blocker.unblock().
    """
    user = get_user_model()

    with db_blocker.unblock():
        exiting_user = user.objects.filter(email=email).first()
        if exiting_user:
            return exiting_user
        if superuser:
            return user.objects.create_superuser(
                email=email,
                password=password,
                username=username,
                phone=phone,
            )
        else:
            return user.objects.create_user(
                email=email, password=password, phone=phone, username=username
            )


@pytest.fixture(scope="session")
def create_admin(django_db_setup: Any, django_db_blocker: Any) -> User:
    return _get_or_create_user(
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD,
        superuser=True,
        phone=ADMIN_PHONE,
        username=ADMIN_USERNAME,
        db_blocker=django_db_blocker,
    )


@pytest.fixture(scope="session")
def create_user(django_db_setup: Any, django_db_blocker: Any) -> User:
    return _get_or_create_user(
        email=USER_EMAIL,
        password=USER_PASSWORD,
        phone=USER_PHONE,
        username=USER_USERNAME,
        db_blocker=django_db_blocker,
    )


@pytest.fixture(scope="session")
def admin_token_storage():
    return login(email=ADMIN_EMAIL, password=ADMIN_PASSWORD)


@pytest.fixture(scope="session")
def user_token_storage():
    return login(email=USER_EMAIL, password=USER_PASSWORD)


@pytest.fixture(scope="session")
def admin_auth_headers(admin_token_storage: Any) -> dict:
    return {"Authorization": f"Bearer {admin_token_storage['access']}"}


@pytest.fixture(scope="session")
def user_auth_headers(user_token_storage: Any) -> dict:
    return {"Authorization": f"Bearer {user_token_storage['access']}"}
