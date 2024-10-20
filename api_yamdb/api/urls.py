from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    SignupView,
    CreateTokenView
)

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSet, basename='user')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

auth_urls = [
    path("signup/", SignupView.as_view(), name="user-signup"),
    path("token/", CreateTokenView.as_view(), name="token-generation"),
]

urls_v1 = [
    path('', include(router_v1.urls)),
    path("auth/", include(auth_urls)),
    path("api-token-auth/", views.obtain_auth_token),
]

urlpatterns = [
    path('v1/', include(urls_v1)),
]
