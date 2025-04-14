from django.urls import include, path
from rest_framework.routers import DefaultRouter

from book.views import BookViewSet

app_name = "book"
router = DefaultRouter()
router.register("books", BookViewSet, basename="books")
urlpatterns = [
    path("", include(router.urls)),
]
