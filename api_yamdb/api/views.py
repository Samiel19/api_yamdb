from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404

from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer, UserAuthSerializer, UserSerializer
from .permissions import IsAdminOrSuperUser
from users.models import User


class TitleViewSet(ModelViewSet):
    pass


class CategoryViewSet(ModelViewSet):
    pass


class GenreViewSet(ModelViewSet):
    pass



class UserRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = request.data['username']
            email = request.data['email']
            user = User.objects.get(username=username)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Код авторизации YaMDB',
                message=f'Ваш код для авторизации: {confirmation_code}',
                from_email='team62@practicum.com',
                recipient_list=[email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class UserAuthenticationView(APIView):
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
            username = request.data['username']
            confirmation_code = request.data['confirmation_code']
            if not User.objects.filter(username=username).exists():
                return Response(
                    'Нет username - нет печенек',
                    status=status.HTTP_404_NOT_FOUND
                )
            user = User.objects.get(username=username)
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