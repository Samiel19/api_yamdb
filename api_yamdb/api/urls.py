from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserAuthenticationView,
                    UserRegisterView, UserViewSet)

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='users')

router.register(
    'titles', TitleViewSet, basename='titles',
)
router.register(
    'categories', CategoryViewSet, basename='categories',
)
router.register(
    'genres', GenreViewSet, basename='genres',)

router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/',
         UserRegisterView.as_view()),
    path('v1/auth/token/', UserAuthenticationView.as_view()),
]
