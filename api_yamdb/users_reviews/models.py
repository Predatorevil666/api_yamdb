from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


MAX_LENGTH: int = 256

MAX_TEXT_LENGTH = 20


class BaseModel(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование')
    slug = models.SlugField(
        max_length=50,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.'
                   ),
        unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_TEXT_LENGTH]


class Category(BaseModel):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска')   # валидатор для проверки года(kittygram2-serializers)
    description = models.TextField(verbose_name='Описание')
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Жанр'

    )
    category = models.OneToOneField(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
