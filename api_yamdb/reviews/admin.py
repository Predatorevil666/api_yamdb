from django.contrib import admin

from .models import Category, Comment, Genre, Genre_title, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_display_links = ('name',)
    empty_value_display = 'Новая категория'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = 'Новый комментарий'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_display_links = ('name',)
    empty_value_display = 'Новый жанр'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')
    list_editable = ('genre',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    search_fields = ('text', 'score', 'author',)
    list_filter = ('pub_date',)
    empty_value_display = 'Новый отзыв'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    list_display_links = ('name',)
    list_editable = ('category',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Genre_title, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
