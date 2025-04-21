from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from user.views import CreateUserView, UserView

app_name = "user"
router = DefaultRouter()
router.register("me", UserView, basename="my_profile")
urlpatterns = [
    path("users/token/", TokenObtainPairView.as_view(), name="get_JWT_token"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", CreateUserView.as_view(), name="register"),
    path("users/", include(router.urls)),
]
