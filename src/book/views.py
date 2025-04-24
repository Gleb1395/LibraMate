from rest_framework.viewsets import ModelViewSet

from book.models import Book
from book.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        return queryset.distinct()
