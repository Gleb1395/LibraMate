from rest_framework import serializers

from borrowing.serializers import BorrowingRetrieveSerializer
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentDetailSerializer(serializers.ModelSerializer):
    borrowing = BorrowingRetrieveSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )
