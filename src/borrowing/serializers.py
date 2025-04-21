from rest_framework import serializers

from book.serializers import BookSerializer
from borrowing.models import Borrowing
from user.serializers import UserRetrieveUpdateSerializer


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(
        read_only=True,
        slug_field="title",
    )

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="email",
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
            "fee",
        )


class BorrowingRetrieveSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
            "fee",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
            "fee",
        )
