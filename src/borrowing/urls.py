from django.urls import include, path
from rest_framework.routers import DefaultRouter

from book.views import BookViewSet
from borrowing.views import BorrowingView

app_name = "borrowing"
router = DefaultRouter()
router.register("borrowings", BorrowingView, basename="borrowings")
urlpatterns = [
    path("", include(router.urls)),
]
