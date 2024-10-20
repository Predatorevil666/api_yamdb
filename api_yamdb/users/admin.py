from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


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
        (_('Информация о пользователе'), {'fields': (
            'first_name',
            'last_name',
            'email',
            'bio',
        )}),
        (_('Разрешения'), {'fields': (
            'is_active',
            'role'
        )}),
        (_('Активность'), {'fields': (
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


admin.site.register(User, UserAdmin)
