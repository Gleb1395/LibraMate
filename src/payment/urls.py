from django.urls import path
from rest_framework.routers import DefaultRouter

from payment.views import (
    CreateCheckoutSessionView,
    payment_cancel,
    payment_success,
    PaymentSessionListView,
    PaymentDetailView,
)

app_name = "payment"
router = DefaultRouter()

urlpatterns = [
    path(
        "create-checkout-session/<int:pk>/",
        CreateCheckoutSessionView.as_view(),
        name="create_checkout_session",
    ),
    path("success/", payment_success, name="payment_success"),
    path("cancel/", payment_cancel, name="payment_cancel"),
    path("payment-list/", PaymentSessionListView.as_view(), name="payment_list"),
    path(
        "payment-detail/<int:pk>/", PaymentDetailView.as_view(), name="payment_detail"
    ),
]
