from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/v1/book/", include("book.urls", namespace="book")),
        path("api/v1/user/", include("user.urls", namespace="user")),
        path("api/v1/borrowing/", include("borrowing.urls", namespace="borrowing")),
        path("api/v1/payment/", include("payment.urls", namespace="payment")),
    ]
    + debug_toolbar_urls()  # NOQA W503
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # NOQA W503
)
