from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.filters import TitleFilter
from api.mixins import (BaseViewSet,
                        CategoryGenreViewSet)
from api.permissions import (IsAdmin,
                             IsAdminOrReadOnly)
from api.serializers import (CategorySerializer,
                             CommentSerializer,
                             CreateTokenSerializer,
                             GenreSerializer,
                             ReviewSerializer,
                             SignupSerializer,
                             TitleCreateSerializer,
                             TitleReadSerializer,
                             UserSerializer)
from reviews.models import (Category,
                            Genre,
                            Review,
                            Title)


User = get_user_model()


class ReviewViewSet(BaseViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        """Получение произведения."""
        return get_object_or_404(
            Title,
            pk=self.kwargs['title_id']
        )

    def get_queryset(self):
        """Получение отзывов на произведение."""
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создание отзыва."""
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(BaseViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        """Получение отзыва."""
        return get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )

    def get_queryset(self):
        """Получение комментариев по отзыву."""
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        """Создание отзыва."""
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'delete', 'patch')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        """
        Получение и обновление данных текущего пользователя.

        GET запрос возвращает данные текущего пользователя.
        PATCH запрос обновляет данные текущего пользователя.
        """
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(request.user,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class SignupView(CreateAPIView):
    """Класс для регистрации новых пользователей."""

    serializer_class = SignupSerializer
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTokenView(CreateAPIView):
    """Класс создания токена для авторизации."""

    serializer_class = CreateTokenSerializer
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response({"token": token["access"]}, status=status.HTTP_200_OK)
