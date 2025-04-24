import datetime
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from book.models import Book
from borrowing.models import Borrowing


class TestBorrowingModel(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="admin",
            username="admin",
            phone="+380888888888",
        )
        self.book = Book.objects.create(
            title="Test Title",
            author="Test Author",
            cover=Book.Cover.HARD,
            inventory=50,
            daily_fee=10,
        )
        self.borrow = Borrowing.objects.create(
            expected_return_date=datetime.date(2025, 6, 22),
            book=self.book,
            user=self.user,
            is_active=True,
        )

    def test_string_representation(self):
        """Test that the string representation of a borrow is correct."""
        self.assertEqual(str(self.borrow), f"Borrowing id {self.borrow.id}")

    def test_expected_return_more_than_borrow_date(self):  # TODOD дать нормальное имя
        """
        Test that a ValidationError is raised if the expected return date
        is earlier than the borrow date.
        """
        self.borrow.borrow_date = datetime.date(2025, 6, 22)
        self.borrow.expected_return_date = datetime.date.today()

        with self.assertRaises(ValidationError):
            self.borrow.clean()

    def test_calculate_total_fee_when_book_returned_on_expected_date(self):
        """
        Test that the total fee is correctly calculated when the book is returned on the expected return date.
        """

        self.assertEqual(self.borrow.fee, None)

        self.borrow.borrow_date = datetime.date(2025, 4, 24)
        date_return = datetime.date(2025, 6, 22)

        self.borrow.expected_return_date = date_return
        self.borrow.actual_return_date = date_return

        self.assertEqual(self.borrow.calculate_total_fee, 590)

    def test_calculate_total_fee_when_book_returned_on_actual_date(self):
        """
        Test that the total fee is calculated based on the actual return date
        when the book is returned earlier than the expected return date.
        """
        self.assertEqual(self.borrow.fee, None)

        self.borrow.borrow_date = datetime.date(2025, 4, 24)

        self.borrow.expected_return_date = datetime.date(2025, 6, 22)
        self.borrow.actual_return_date = datetime.date(2025, 6, 15)

        self.assertEqual(self.borrow.calculate_total_fee, 520)

    def test_calculate_total_fee_when_book_not_returned_yet(self):
        """
        Test that the total fee is zero when the book has not been returned yet (actual return date is None).
        """
        self.assertEqual(self.borrow.fee, None)

        self.borrow.borrow_date = datetime.date(2025, 4, 24)
        self.borrow.expected_return_date = datetime.date(2025, 6, 22)

        self.assertEqual(self.borrow.actual_return_date, None)
        self.assertEqual(self.borrow.calculate_total_fee, 0.00)

    def test_save_calls_decrease_inventory_on_creation(self):
        """
        Test that the decrease_inventory() method is called
        when a new Borrowing instance is created.
        """
        with patch.object(Book, "decrease_inventory") as mock_decrease:
            borrowing = Borrowing.objects.create(
                book=self.book,
                user=self.user,
                borrow_date=datetime.date(2025, 4, 24),
                expected_return_date=datetime.date(2025, 6, 22),
            )  # NOQA F841
            mock_decrease.assert_called_once()

    def test_save_on_book_return_sets_fee_and_increases_inventory(self):
        """
        Test that upon setting actual_return_date and saving:
        - increase_inventory() is called,
        - is_active is set to False,
        - and the total fee is calculated correctly.
        """
        borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            borrow_date=datetime.date(2025, 4, 24),
            expected_return_date=datetime.date(2025, 6, 22),
        )
        with patch.object(Book, "increase_inventory") as mock_increase:
            borrowing.actual_return_date = datetime.date(2025, 6, 22)
            borrowing.save()

            mock_increase.assert_called_once()
            self.assertFalse(borrowing.is_active)
            self.assertEqual(borrowing.fee, 590)

    def test_save_does_nothing_if_not_returned(self):
        """
        Test that saving a borrowing without an actual return date:
        - does not call increase_inventory(),
        - leaves is_active as True,
        - and fee remains None.
        """
        borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            borrow_date=datetime.date(2025, 4, 24),
            expected_return_date=datetime.date(2025, 6, 22),
        )

        with patch.object(Book, "increase_inventory") as mock_increase:
            borrowing.save()
            mock_increase.assert_not_called()
            self.assertTrue(borrowing.is_active)
            self.assertIsNone(borrowing.fee)
