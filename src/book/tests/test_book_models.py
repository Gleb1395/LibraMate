from django.core.exceptions import ValidationError
from django.test import TestCase

from book.models import Book


class TestBook(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Title",
            author="Test Author",
            cover=Book.Cover.HARD,
            inventory=50,
            daily_fee=10,
        )

    def test_string_representation(self):
        """Test that the string representation of a book is correct."""
        self.assertEqual(str(self.book), "Book Test Title")

    def test_increase_inventory(self):
        """Test that increasing inventory increments the count by 1."""
        self.assertEqual(self.book.inventory, 50)
        self.book.increase_inventory()
        self.assertEqual(self.book.inventory, 51)

    def test_decrease_inventory(self):
        """Test that decreasing inventory decrements the count by 1."""
        self.assertEqual(self.book.inventory, 50)
        self.book.decrease_inventory()
        self.assertEqual(self.book.inventory, 49)

    def test_decrease_inventory_below_zero_raises_error(self):
        """Test that decreasing inventory below zero raises a ValidationError."""
        self.book.inventory = 0
        with self.assertRaises(ValidationError):
            self.book.decrease_inventory()

    def test_negative_inventory_validation(self):
        """Test that validation fails if inventory is set to a negative value."""
        self.book.inventory = -1
        with self.assertRaises(ValidationError):
            self.book.clean()
