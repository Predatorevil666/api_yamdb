from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.constants import CONFIRMATION_LENGTH, EMAIL_LENGTH, USERNAME_LENGTH
from users.roles import Roles
from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_LENGTH,
        unique=True,
        error_messages={
            'unique': "Пользователь с таким именем уже существует.",
        },
        validators=[
            UnicodeUsernameValidator(),
            validate_username,
        ],
    )
    email = models.EmailField(
        'Адрес электронной почты',
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
        'Информация о пользователе',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role.value) for role in Roles),
        choices=Roles.choices,
        default=Roles.USER.value
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """
        Переопределенный метод сохранения для модели User.

        Автоматически устанавливает права доступа пользователя
        в зависимости от его роли и статуса суперпользователя.

        - Если роль пользователя - ADMIN или
        пользователь является суперпользователем, то устанавливает флаги
        is_staff и is_superuser в True.
        - Для всех остальных ролей эти флаги устанавливаются в False.
        """

        if self.role == Roles.ADMIN.value or self.is_superuser:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        """
        Свойство,
        которое проверяет, является ли пользователь администратором.
        """
        return self.role == (
            Roles.ADMIN.value
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        """
        Свойство, которое проверяет, является ли пользователь модератором.
        """
        return self.role == Roles.MODERATOR.value

    @property
    def generate_confirmation_token(self):
        """
        Генерирует токен подтверждения для пользователя.
        """
        return default_token_generator.make_token(self)

    def check_confirmation_token(self, token):
        """
        Проверяет токен подтверждения для пользователя.
        """
        return default_token_generator.check_token(self, token)
