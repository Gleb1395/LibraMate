from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    """
    Represents a payment made for a borrowing instance.

    Attributes:
        status (str): The current payment status. Options:
            - PENDING: Payment has not yet been completed.
            - PAID: Payment was completed successfully.
        type (str): The type of payment. Options:
            - PAYMENT: Regular payment.
            - FINE: A fine due to overdue return.
        borrowing (Borrowing): The borrowing this payment is linked to.
        session_url (str): URL of the payment session (e.g., Stripe checkout).
        session_id (str): ID of the payment session.
        money_to_pay (Decimal): The total amount due for the borrowing or fine.
    """

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
    objects = models.Manager()
