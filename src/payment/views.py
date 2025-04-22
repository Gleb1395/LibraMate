import stripe
from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from borrowing.models import Borrowing
from config import settings
from payment.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(APIView):
    def post(self, request, pk):
        borrowing_id = pk
        borrowing = Borrowing.objects.get(id=borrowing_id)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(borrowing.book.daily_fee * 100),
                    "product_data": {
                        "name": borrowing.book.title,
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=request.build_absolute_uri(
                reverse("payment:payment_success")
            ),
            cancel_url=request.build_absolute_uri(
                reverse("payment:payment_cancel")
            ),
            metadata={
                "borrowing_id": borrowing_id,
            }
        )
        print(f"id session: {checkout_session.id}")
        print(f"session url: {checkout_session.url}")
        print(f"session status: {checkout_session.status}")

        return Response({"checkout_url": checkout_session.url}, status=status.HTTP_200_OK)


@api_view(["GET"])
def payment_success(request: HttpRequest) -> Response:
    print(request.data)
    print(request.query_params)
    return Response({"detail": "Payment was successful! Thank you."}, status=status.HTTP_200_OK)


@api_view(["GET"])
def payment_cancel(request: HttpRequest) -> Response:
    return Response({"detail": "The payment has been cancelled. You can try again."}, status=status.HTTP_200_OK)
