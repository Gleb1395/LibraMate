from django.core.management import call_command
import os
import pytest
import random
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from typing import Any
from dotenv import load_dotenv

from book.models import Book
from tests.services.book.api_books import BooksAPI
from tests.utils.auth import login
from faker import Faker


fake = Faker("uk_UA")
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


# @pytest.fixture(autouse=True)
# def set_test_host_env(live_server, monkeypatch):
#     """
#     Устанавливаем переменную окружения HOST = live_server.url + '/api/v1/book'
#     до инициализации любых Endpoint-ов.
#     """
#     test_host = f"{live_server.url}/api/v1/book"
#     monkeypatch.setenv("HOST", test_host)


# @pytest.fixture
# def endpoint(live_server):
#     """Raises a test HTTP server (live_server.url), creates endpoints on that server, and returns BooksAPI."""
#     test_host = f"{live_server}"
#     endpoint = GlobalEndpoint(host=test_host)
#     return endpoint


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


def _create_lists_books(count: int, db_blocker) -> None:
    """Populate the test database with `count` random Book records."""
    with db_blocker.unblock():
        books = []
        for _ in range(count):
            books.append(
                Book(
                    title=fake.text(max_nb_chars=20),
                    author=fake.full_name(),
                    cover=random.choice([Book.Cover.HARD, Book.Cover.SOFT]),
                    inventory=random.randint(20, 100),
                    daily_fee=round(random.uniform(2.0, 15.0), 2),
                )
            )
        Book.objects.bulk_create(books)


@pytest.fixture(scope="session")
def create_books(django_db_setup: Any, django_db_blocker: Any) -> None:
    """Create 100 random Book entries once per test session."""
    return _create_lists_books(100, django_db_blocker)


@pytest.fixture(scope="session")
def create_admin(django_db_setup: Any, django_db_blocker: Any) -> User:
    """Create or get a superuser for tests."""
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
    """Create or get a regular user for tests."""
    return _get_or_create_user(
        email=USER_EMAIL,
        password=USER_PASSWORD,
        phone=USER_PHONE,
        username=USER_USERNAME,
        db_blocker=django_db_blocker,
    )


@pytest.fixture(scope="session")
def admin_token_storage():
    """Authenticate as admin and return JWT tokens."""
    return login(email=ADMIN_EMAIL, password=ADMIN_PASSWORD)


@pytest.fixture(scope="session")
def user_token_storage():
    """Authenticate as user and return JWT tokens."""
    return login(email=USER_EMAIL, password=USER_PASSWORD)


@pytest.fixture(scope="session")
def admin_auth_headers(admin_token_storage: Any) -> dict:
    """Provide HTTP headers with admin's access token."""
    return {"Authorization": f"Bearer {admin_token_storage['access']}"}


@pytest.fixture(scope="session")
def user_auth_headers(user_token_storage: Any) -> dict:
    """Provide HTTP headers with admin's access token."""
    return {"Authorization": f"Bearer {user_token_storage['access']}"}
