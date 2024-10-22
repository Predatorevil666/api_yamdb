from rest_framework import status, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.response import Response
from api.permissions import (IsAdminOrReadOnly,
                             IsAuthorOrReadOnly)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter


class BaseViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'delete', 'patch']

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Метод не разрешен"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Общий класс для CategoryViewSet и GenreViewSet."""
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
