from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    CommentViewSet
    UserViewSet
)

from .views import UserRegisterView, UserAuthenticationView


app_name = 'api'

router = SimpleRouter()

router.register(
    'titles', TitleViewSet, basename='titles',
)
router.register(
    'categories', CategoryViewSet, basename='categories',
)
router.register(
    'genres', GenreViewSet, basename='genres',

router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')

router.register(
    r'titles/(?P<title_id>\d+)/'
    r'reviews/(?P<review_id>\d+/comments/(?P<comment_id>\d+/',
    CommentViewSet, basename='comment')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/',
        UserRegisterView.as_view()),
    path('v1/auth/token/', UserAuthenticationView.as_view()),
]
