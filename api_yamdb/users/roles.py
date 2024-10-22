from django.db import models


class Roles(models.TextChoices):
    USER = 'user', 'пользователь'
    MODERATOR = 'moderator', 'модератор'
    ADMIN = 'admin', 'администратор'
