from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    """
    The book model represent a book in the library catalog
    Attributes:
        title (str): The title of the book
        author (str): The author of the book
        cover (str): The cover of the book:
            - 1 (HARD): Hard cover
            - 2 (SOFT): Soft cover
        inventory (int): The number of available copies of the book. Cannot be negative.
        daily_fee (decimal): The daily rental fee for the book in US dollars. Cannot be negative.
    """

    class Cover(models.IntegerChoices):
        HARD = 1
        SOFT = 2

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.SmallIntegerField(choices=Cover.choices, default=Cover.HARD)
    inventory = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)]) # TODO Realize this count
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
