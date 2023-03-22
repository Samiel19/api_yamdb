from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import validate_username
from api_yamdb.settings import ROLES, ROLES_MAX_LEN, DEFAUL_ROLE


NAMES_MAX_LEN = 150
EMAIL_MAX_LEN = 254


class User(AbstractUser):
    role = models.CharField(
        choices=ROLES,
        max_length=ROLES_MAX_LEN,
        blank=False,
        verbose_name='Роль',
        default=DEFAUL_ROLE
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LEN,
        verbose_name='Почта',
        unique=True
    )
    username = models.CharField(
        max_length=NAMES_MAX_LEN,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[validate_username]
    )
    first_name = models.CharField(
        max_length=NAMES_MAX_LEN,
        verbose_name='Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=NAMES_MAX_LEN,
        verbose_name='Фамилия',
        blank=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
