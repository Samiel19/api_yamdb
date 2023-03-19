from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, filters, permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer, UserAuthSerializer, UserSerializer
from .serializers import (
    ReviewSerializers, CommentSerializers,
    TitleReadSerializer, TitleWriteSerializer,
    CategorySerializer, GenreSerializer,
    UserRegisterSerializer, UserAuthSerializer, UserSerializer,
)
from .permissions import IsAdminOrSuperUser, IsAuthenticatedUser, AdminOrReadOnly
from .filters import TitleFilter
from reviews.models import Review, Comment, Title, Category, Genre
from users.models import User


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
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
        if serializer.is_valid():
            serializer.save()
            username = request.data['username']
            user = User.objects.get(username=username)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Код авторизации YaMDB',
                message=f'Ваш код для авторизации: {confirmation_code}',
                from_email='team62@practicum.com',
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif User.objects.filter(
            email=request.data.get('email'),
            username=request.data.get('username')
        ).exists():
            username = request.data['username']
            user = User.objects.get(username=username)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Код авторизации YaMDB',
                message=f'Ваш код для авторизации: {confirmation_code}',
                from_email='team62@practicum.com',
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
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
            confirmation_code = serializer.validated_data.get('confirmation_code')
            if not User.objects.filter(username=username).exists():
                return Response(
                    'Нет username - нет печенек',
                    status=status.HTTP_404_NOT_FOUND
                )
            user = get_object_or_404(User, username=username)
            if not default_token_generator.check_token(user, confirmation_code):
                return Response(
                    'Не верный код подтверждения',
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
    def get_titles(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, titles=self.get_titles)

    def get_queryset(self):
        return self.get_titles.reviews.all()

    # def post(self, request):
    #     serializer = ReviewSerializers(data=request.data)
    #     if serializer.is_valid():
    #         if Review.objects.filter(reviews=request.data.get('reviews'),
    #                                  username=request.data.get('username')
    #                                  ).exists():
    #             return Response(
    #                 'Нелзя',
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #     return Response(serializer.data)

    # @action(
    #     methods=['post'],
    #     detail=False,
    #     permission_classes=[IsAuthenticatedUser],
    # )
    # def post(self, request, *args, **kwargs):
    #     # if request.method == 'POST':
    #     #     serializer = ReviewSerializers(data=request.data)
    #     #     if serializer.is_valid(raise_exception=True):
    #     #         return Response(serializer.validated_data, status=status.HTTP_200_OK)
    #     #     else:
    #     #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializer = ReviewSerializers(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
