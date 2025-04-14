from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from book.models import Book
from user.models import Customer


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(auto_now=False, auto_now_add=False)
    actual_return_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def clean(self):
        if self.expected_return_date and self.borrow_date:
            if self.expected_return_date < self.borrow_date:
                raise ValidationError("Expected return date cannot be earlier than borrow date.")

    @property
    def calculate_total_fee(self):
        if self.actual_return_date:
            daily_fee = self.book.daily_fee
            total_days = (self.actual_return_date - self.borrow_date).days
            total_fee = daily_fee * total_days
            return total_fee
        return Decimal("0.00")

    def save(self, *args, **kwargs):
        if self.actual_return_date and self.fee is None:
            self.fee = self.calculate_total_fee
        if self.actual_return_date:
            self.is_active = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Borrowing"
        verbose_name_plural = "Borrowings"

    def __str__(self):
        return f"Borrowing id {self.id}"
