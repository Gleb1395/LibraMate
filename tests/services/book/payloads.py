import os
import django


import random
from book.models import Book
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


fake = Faker("uk_UA")


class BookPayloads:
    @staticmethod
    def create_book():
        return {
            "title": fake.text(max_nb_chars=20),
            "author": fake.full_name(),
            "cover": random.choice(
                [Book.Cover.HARD, Book.Cover.SOFT]
            ),  # TODO Как правильно
            "inventory": random.randint(20, 100),
            "daily_fee": round(random.uniform(2.0, 15.0), 2),
        }
