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


class CategoryViewSet(CreateModelMixin, ListModelMixin,
                      DestroyModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    permission_classes = (AdminOrReadOnly,)
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(CreateModelMixin, ListModelMixin,
                   DestroyModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    permission_classes = (AdminOrReadOnly,)
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

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
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(**serializer.validated_data)
            send_code(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif User.objects.filter(
            email=email,
            username=request.data.get('username')
        ).exists():
            user = User.objects.get(username=username, email=email)
            send_code(user=user)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code'
            )
            if not User.objects.filter(username=username).exists():
                return Response(
                    'Нет username - нет печенек',
                    status=status.HTTP_404_NOT_FOUND
                )
            user = get_object_or_404(User, username=username)
            if not default_token_generator.check_token(
                user, confirmation_code
            ):
                return Response(
                    'Неверный код подтверждения',
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = self.get_tokens_for_user(user)
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        methods=['get'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
    )
    def get_me(self, request):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['patch'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
    )
    def patch(self, request):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(
            user, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializers
    permission_classes = (IsAuthenticatedUser, IsAuthenticatedOrReadOnly,)

    @property
    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title)

    def get_queryset(self):
        return self.get_title.reviews.all()

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = ReviewSerializers(data=request.data)
            if serializer.is_valid(raise_exception=True):
                return Response(
                    serializer.validated_data, status=status.HTTP_200_OK
                )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = (IsAuthenticatedUser, IsAuthenticatedOrReadOnly,)

    @property
    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review)

    def get_queryset(self):
        return self.get_review.comments.all()
