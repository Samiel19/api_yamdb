from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    roles = [
        'user',
        'moderator',
        'admin',
    ]
    role = models.CharField(
        max_length=100,
        choices=roles,
        blank=False,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    username = models.CharField(
        max_length=150,
        unique=True
        )