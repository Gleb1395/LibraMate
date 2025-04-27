from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.permissions import IsAdminOrIfAuthenticatedReadOnly
from borrowing.serializers import (
    BorrowingCreateSerializer,
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
    BorrowingFilterSerializer,
)


class BorrowingView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all().select_related("book", "user")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingListSerializer

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if not self.request.user.is_authenticated:
            return queryset.none()

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        else:
            if user_id is not None:
                queryset = queryset.filter(user_id=user_id)

        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    @extend_schema(parameters=[BorrowingFilterSerializer])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def return_(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date:
            return Response(
                {"detail": "Book already returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowing.actual_return_date = timezone.now().date()
        borrowing.is_active = False
        borrowing.book.increase_inventory()
        borrowing.book.save()
        borrowing.save()
        return Response({"detail": "Book returned successfully."}, status=200)
