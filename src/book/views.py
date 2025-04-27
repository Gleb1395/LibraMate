from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from book.models import Book
from book.permissions import OpenListPrivateDetailPermission
from book.serializers import BookSerializer, BookFilterSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (OpenListPrivateDetailPermission,)

    def get_queryset(self):
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        return queryset.distinct()

    @extend_schema(parameters=[BookFilterSerializer])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
