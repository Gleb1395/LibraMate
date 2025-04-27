from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from book.models import Book
from user.models import Customer


class Borrowing(models.Model):
    """
    Represents a book borrowing record made by a user.

    Attributes:
        borrow_date (date): The date when the book was borrowed. Automatically set on creation.
        expected_return_date (date): The date by which the book is expected to be returned.
        actual_return_date (date, optional): The date when the book was actually returned.
        book (Book): The book that was borrowed.
        user (Customer): The user who borrowed the book.
        is_active (bool): Indicates whether the borrowing is currently active.
        fee (Decimal, optional): The total fee calculated based on the borrowing duration.

    Methods:
        clean(): Ensures the expected return date is not before the borrow date.
        calculate_total_fee (property): Calculates the total rental fee based on the borrowing duration.
        save(): Automatically adjusts inventory and calculates the fee if needed.
    """

    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(auto_now=False, auto_now_add=False)
    actual_return_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.expected_return_date and self.borrow_date:
            if self.expected_return_date < self.borrow_date:
                raise ValidationError("Expected return date cannot be earlier than borrow date.")

    @property
    def calculate_total_fee(self):
        daily_fee = self.book.daily_fee

        if self.expected_return_date == self.actual_return_date:
            total_days = (self.expected_return_date - self.borrow_date).days
        elif self.actual_return_date:
            total_days = (self.actual_return_date - self.borrow_date).days
        else:
            return Decimal("0.00")
        total_fee = daily_fee * total_days
        return total_fee

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if is_new:
            self.book.decrease_inventory()

        elif self.actual_return_date and self.is_active:
            self.book.increase_inventory()
            self.is_active = False

            if self.fee is None:
                self.fee = self.calculate_total_fee

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Borrowing"
        verbose_name_plural = "Borrowings"

    def __str__(self):
        return f"Borrowing id {self.id}"
