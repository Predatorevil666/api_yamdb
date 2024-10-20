from rest_framework import filters, viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from api.permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Общий класс для CategoryViewSet и GenreViewSet."""
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
