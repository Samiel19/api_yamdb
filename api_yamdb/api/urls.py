from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (TitleViewSet, CategoryViewSet,
    GenreViewSet)


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
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
