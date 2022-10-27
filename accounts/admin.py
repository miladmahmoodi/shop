from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import (
    User as UserModel,
    OtpCode as OtpCodeModel,
)
from . import forms


class UserAdmin(BaseUserAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    list_display = (
        'phone_number',
        'email',
        'full_name',
        'is_admin',
    )
    list_filter = (
        'is_admin',
    )

    fieldsets = (
        (None, {'fields': (
            'phone_number',
            'password',
        )}),
        ('Personal Info', {'fields': (
            'email',
            'full_name',
            'last_login',
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_admin',     #is_staff
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        ('Create Account', {'fields': (
            'phone_number',
            'email',
            'full_name',
            'password',
            'confirm_password',
        )}),
    )
    search_fields = (
        'phone_number',
        'email',
    )
    ordering = (
        'email',
    )
    filter_horizontal = (
        'groups',
        'user_permissions',
    )
    readonly_fields = (
        'last_login',
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_super = request.user.is_superuser
        if not is_super:
            form.base_fields['is_superuser'].disabled = True
        return form


@admin.register(OtpCodeModel)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = (
        'phone_number',
        'code',
        'created_at',
    )


# admin.site.unregister(Group)
admin.site.register(UserModel, UserAdmin)
