from django.contrib import admin

from .models import Category, Title, Genre


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_display_links = ('name',)
    empty_value_display = 'Новая категория'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'genre',
        'category',
    )
    search_fields = ('name',)
    list_display_links = ('name',)
    list_editable = ('category',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_display_links = ('name',)
    empty_value_display = 'Новый жанр'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
