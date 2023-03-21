from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.settings import ROLES, ROLES_MAX_LEN


NAMES_MAX_LEN = 150
EMAIL_MAX_LEN = 254


class User(AbstractUser):
    role = models.CharField(
        choices=ROLES,
        max_length=ROLES_MAX_LEN,
        blank=False,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LEN,
        unique=True
    )
    username = models.CharField(
        max_length=NAMES_MAX_LEN,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    first_name = models.CharField(
        max_length=NAMES_MAX_LEN,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=NAMES_MAX_LEN,
        verbose_name='фамилия',
        blank=True
    )
