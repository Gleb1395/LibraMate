from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class PaymentStatus(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINED = "FINE", "Fine"

    status = models.CharField(choices=Status.choices, default=Status.PENDING, max_length=50)
    type = models.CharField(choices=PaymentStatus.choices, default=PaymentStatus.PAYMENT, max_length=50)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=50)
    money_to_pay = models.DecimalField(decimal_places=2, max_digits=10)
