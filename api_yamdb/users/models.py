from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from users.roles import Roles

from users.constants import (
    EMAIL_LENGTH,
    ROLE_LENGTH,
    USERNAME_LENGTH,
)


class User(AbstractUser):
    username = models.CharField(
        max_length=USERNAME_LENGTH,
        unique=True,
        error_messages={
            'unique': "Пользователь с таким именем уже существует.",
        },
        validators=[
            UnicodeUsernameValidator(),
        ],
    )
    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        unique=True
    )
    first_name = models.CharField(
        max_length=USERNAME_LENGTH,
        blank=True

    )
    last_name = models.CharField(
        max_length=USERNAME_LENGTH,
        blank=True

    )
    bio = models.TextField(
        blank=True
    )
    role = models.CharField(
        max_length=ROLE_LENGTH,
        choices=Roles.choices,
        default=Roles.USER
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        """
        Свойство,
        которое проверяет, является ли пользователь администратором.
        """
        return self.role == Roles.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        """
        Свойство, которое проверяет, является ли пользователь модератором.
        """
        return self.role == Roles.MODERATOR
