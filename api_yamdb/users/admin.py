from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'date_joined'
    )
    search_fields = (
        'username__icontains',
        'email__icontains',
        'first_name__icontains',
        'last_name__icontains'
    )
    list_filter = (
        'role',
        'date_joined'
    )
    ordering = (
        '-date_joined',
    )

    fieldsets = (
        (None, {'fields': (
            'username',
            'password'
        )}),
        ('Информация о пользователе', {'fields': (
            'first_name',
            'last_name',
            'email',
            'bio',
        )}),
        ('Разрешения', {'fields': (
            'is_active',
            'role'
        )}),
        ('Активность', {'fields': (
            'last_login',
            'date_joined'
        )}),
    )

    add_fieldsets = (
        (None, {'fields': (
            'username',
            'email',
            'password1',
            'password2',
            'role'
        )}),
    )
    readonly_fields = (
        'date_joined',
    )


admin.site.unregister(Group)
