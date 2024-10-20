from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.roles import Roles

from users.constants import (
    EMAIL_LENGTH,
    ROLE_LENGTH,
    USERNAME_LENGTH,
)


class User(AbstractUser):
    username = models.CharField(
        _('Имя пользователя'),
        max_length=USERNAME_LENGTH,
        unique=True,
        error_messages={
            'unique': _("Пользователь с таким именем уже существует."),
        },
        validators=[
            UnicodeUsernameValidator(),
        ],
    )
    email = models.EmailField(
        _('Адрес электронной почты'),
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
        _('Информация о пользователе'),
        blank=True
    )
    role = models.CharField(
        _('Роль'),
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

    def save(self, *args, **kwargs):
        """
        Переопределенный метод сохранения для модели User.

        Автоматически устанавливает права доступа пользователя
        в зависимости от его роли.
        Если роль пользователя - ADMIN,
        то устанавливает флаги is_staff и is_superuser в True.
        Для всех остальных ролей эти флаги устанавливаются в False.
        """

        if self.role == Roles.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

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
