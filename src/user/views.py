from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from borrowing.permissions import IsAdminOrIfAuthenticatedReadOnly
from user.serializers import (
    MyTokenObtainPairSerializer,
    UserRetrieveUpdateSerializer,
    UserSerializer,
    UserListRetrieveSerializer,
)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = serializer.data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = get_user_model().objects.all()
    serializer_class = UserRetrieveUpdateSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get("id")

        if not self.request.user.is_authenticated:
            return queryset.none()

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        else:
            if user_id is not None:
                queryset = queryset.filter(user_id=id)

        return queryset

    @extend_schema(parameters=[UserListRetrieveSerializer])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
