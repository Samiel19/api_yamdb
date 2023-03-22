from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title

from users.models import User

from .filters import TitleFilter
from .permissions import (AdminOrReadOnly, IsAdminOrSuperUser,
                          IsAuthenticatedUser)
from .serializers import (CategorySerializer, CommentSerializers,
                          GenreSerializer, ReviewSerializers,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserAuthSerializer, UserRegisterSerializer,
                          UserSerializer)
from .utils import send_code


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (AdminOrReadOnly, IsAuthenticatedUser,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryGenreViewSet(CreateModelMixin, ListModelMixin,
                           DestroyModelMixin, GenericViewSet):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        if User.objects.filter(
            email=email,
            username=username
        ).exists():
            user = User.objects.get(username=username, email=email)
            send_code(user=user)
            return Response(status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(**serializer.validated_data)
        send_code(user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAuthenticationView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'acesses': str(refresh.access_token),
        }

    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data.get(
            'confirmation_code'
        )
        if not default_token_generator.check_token(user,
                                                   confirmation_code):
            return Response('Неверный код подтверждения',
                            status=status.HTTP_400_BAD_REQUEST)
        token = self.get_tokens_for_user(user)
        return Response(token, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = [
        'get',
        'patch',
        'delete',
        'head',
        'post'
    ]

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
    )
    def patch_me(self, request):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user,
                                    data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializers
    permission_classes = (IsAuthenticatedUser, IsAuthenticatedOrReadOnly,)

    @property
    def title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title)

    def get_queryset(self):
        return self.title.reviews.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = (IsAuthenticatedUser, IsAuthenticatedOrReadOnly,)

    @property
    def review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review)

    def get_queryset(self):
        return self.review.comments.all()
