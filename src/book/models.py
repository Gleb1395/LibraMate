from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


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
    inventory = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["title"]
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"Book {self.title}"

    def clean(self):
        super().clean()
        if self.inventory < 0:
            raise ValidationError("Inventory cannot be negative.")

    def increase_inventory(self):
        self.inventory += 1
        self.save()

    def decrease_inventory(self):
        self.inventory -= 1
        if self.inventory < 0:
            raise ValidationError("Inventory cannot be negative.")
        self.save()
