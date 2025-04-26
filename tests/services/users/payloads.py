import random

from faker import Faker
import phonenumbers

fake = Faker("uk_UA")


def random_ua_phone() -> str:
    subscriber = "".join(str(random.randint(0, 9)) for _ in range(7))
    return f"+38095{subscriber}"


class Payloads:
    password = fake.password(length=10)

    create_user = {
        "email": fake.email(),
        "password": password,
        "password2": password,
        "username": fake.user_name(),
        "phone": random_ua_phone(),
    }
