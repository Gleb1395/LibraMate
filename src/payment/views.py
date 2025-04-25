import stripe
from django.db import transaction
from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils.representation import serializer_repr
from rest_framework.views import APIView

from borrowing.models import Borrowing
from config import settings
from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentDetailSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(APIView):
    def post(self, request, pk):
        borrowing_id = pk

        try:
            borrowing = Borrowing.objects.get(id=borrowing_id)
        except Borrowing.DoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        exist_payment = Payment.objects.filter(
            status=Payment.Status.PENDING, borrowing=borrowing
        ).first()
        if exist_payment:
            return Response(
                {
                    "detail": "Pending payment already exists",
                    "checkout_url": exist_payment.session_url,
                },
                status=status.HTTP_200_OK,
            )

        with transaction.atomic():
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": int(borrowing.fee * 100),
                            "product_data": {
                                "name": borrowing.book.title,
                            },
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=request.build_absolute_uri(
                    reverse("payment:payment_success")
                )
                + "?session_id={CHECKOUT_SESSION_ID}",  # NOQA W503
                cancel_url=request.build_absolute_uri(reverse("payment:payment_cancel"))
                + "?session_id={CHECKOUT_SESSION_ID}",  # NOQA W503
                metadata={
                    "borrowing_id": borrowing.id,
                },
            )
            Payment.objects.create(
                status=Payment.Status.PENDING,
                type=Payment.PaymentStatus.PAYMENT,
                borrowing=borrowing,
                session_id=checkout_session.id,
                session_url=checkout_session.url,
                money_to_pay=borrowing.fee,
            )

        return Response(
            {"checkout_url": checkout_session.url}, status=status.HTTP_200_OK
        )


class PaymentSessionListView(APIView):
    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"detail": "You are not logged in, please log in."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if user.is_staff:
            payments = Payment.objects.all()
        else:
            payments = Payment.objects.filter(borrowing__user=user).select_related(
                "borrowing__user"
            )

        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentDetailView(APIView):
    def get(self, request, pk):
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"detail": "You are not logged in, please log in."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        payment = (
            Payment.objects.select_related("borrowing__user").filter(id=pk).first()
        )
        if not payment:
            return Response(
                {"detail": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not user.is_staff and payment.borrowing.user != user:
            return Response(
                {"detail": "Access denied."}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = PaymentDetailSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def payment_success(request: HttpRequest) -> Response:
    session_id = request.query_params.get("session_id")
    payment = Payment.objects.get(session_id=session_id)
    payment.status = Payment.Status.PAID
    payment.save()
    return Response(
        {"detail": "Payment was successful! Thank you."}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def payment_cancel(request: HttpRequest) -> Response:
    session_id = request.query_params.get("session_id")
    payment = Payment.objects.get(session_id=session_id)
    payment.status = Payment.Status.PAID
    payment.type = Payment.PaymentStatus.FINED
    payment.save()
    return Response(
        {"detail": "The payment has been cancelled. You can try again."},
        status=status.HTTP_200_OK,
    )
