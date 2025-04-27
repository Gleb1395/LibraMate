from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Book
from borrowing.models import Borrowing
import datetime

from payment.models import Payment

PAYMENT_LIST_URL = reverse("payment:payment_list")


class BasePaymentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@user.com",
            password="user",
            username="user",
            phone="+380888888811",
        )
        self.user_2 = get_user_model().objects.create_user(
            email="example@user.com",
            password="example",
            username="example",
            phone="+380888888899",
        )
        self.admin = get_user_model().objects.create_superuser(
            password="admin",
            email="admin@admin.com",
        )
        self._create_book()
        self._create_borrowing()
        self._create_payment()

    def _create_book(self):
        self.book_1 = Book.objects.create(
            title="The Python Prophecy",
            author="Ada Lennox",
            cover=Book.Cover.HARD,
            inventory=50,
            daily_fee=10,
        )
        self.book_2 = Book.objects.create(
            title="Django Unleashed",
            author="Carl Rutherford",
            cover=Book.Cover.HARD,
            inventory=50,
            daily_fee=10,
        )

    def _create_borrowing(self):
        self.borrowing_1 = Borrowing.objects.create(
            borrow_date=datetime.date(2025, 4, 25),
            expected_return_date=datetime.date(2025, 4, 29),
            actual_return_date=datetime.date(2025, 4, 29),
            book=self.book_1,
            user=self.user,
        )
        self.borrowing_2 = Borrowing.objects.create(
            borrow_date=datetime.date(2025, 4, 26),
            expected_return_date=datetime.date(2025, 4, 30),
            actual_return_date=datetime.date(2025, 4, 30),
            book=self.book_2,
            user=self.user_2,
        )

    def _create_payment(self):
        self.payment_1 = Payment.objects.create(
            borrowing=self.borrowing_1,
            session_url="https://checkout.stripe.com/example",
            session_id="1",
            money_to_pay=self.borrowing_1.calculate_total_fee,
        )

        self.payment_2 = Payment.objects.create(
            borrowing=self.borrowing_2,
            session_url="https://checkout.stripe.com/example2",
            session_id="2",
            money_to_pay=self.borrowing_1.calculate_total_fee,
        )


class PaymentListViewTests(BasePaymentTestCase):

    def test_list_payments_anonymous_forbidden(self):
        """Test that anonymous user cannot access the payment list."""
        url = PAYMENT_LIST_URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_book_authenticated_allowed(self):
        """Test that authenticated users (admin and regular) can access the payment list."""
        for user in [self.admin, self.user]:
            self.client.force_authenticate(user=user)
            response = self.client.get(PAYMENT_LIST_URL)
            self.assertEqual(
                response.status_code, status.HTTP_200_OK, msg=f"Failed for user: {user}"
            )

    def test_payment_list_visibility_based_on_user_role(self):
        """Test that payment list differs for admin and regular users."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(PAYMENT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.client.force_authenticate(user=self.admin)
        response = self.client.get(PAYMENT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class PaymentRetrieveViewTests(BasePaymentTestCase):
    def test_retrieve_payments_anonymous_forbidden(self):
        """Test that anonymous user cannot access the payment retrieve."""

        url = reverse("payment:payment_detail", args=[self.payment_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_book_authenticated_allowed(self):
        """
        Test that admin and owning user can retrieve payment details,
        while other users receive a 403 Forbidden.
        """

        for user in [self.admin, self.user]:
            self.client.force_authenticate(user=user)
            url = reverse("payment:payment_detail", args=[self.payment_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.user_2)
        url = reverse("payment:payment_detail", args=[self.payment_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
