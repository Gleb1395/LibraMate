from django.urls import path
from rest_framework.routers import DefaultRouter
from payment.views import payment_success, payment_cancel, CreateCheckoutSessionView

app_name = "payment"
router = DefaultRouter()

urlpatterns = [
    path("create-checkout-session/<int:pk>/", CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path("success/", payment_success, name="payment_success"),
    path("cancel/", payment_cancel, name="payment_cancel"),

]