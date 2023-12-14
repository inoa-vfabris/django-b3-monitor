from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from rest_framework import request
from rest_framework.authtoken.models import TokenProxy

from .consts import Role
from .forms import UserChangeForm, UserCreationForm
from .models import Group, User
from .services import user_set_permissions

admin.site.unregister(TokenProxy)
admin.site.unregister(DjangoGroup)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "email",
        "full_name",
        "cpf",
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_active", "role")
    fieldsets = (
        (
            _("informations"),
            {
                "fields": (
                    "id",
                    "full_name",
                    "email",
                    "password",
                    "cpf",
                    "role",
                    "is_active",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("email", "cpf", "role", "password1", "password2")},
        ),
    )
    readonly_fields = ("id", "date_joined", "last_login")
    search_fields = ("email", "full_name", "cpf")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")
    show_full_result_count = False

    def get_readonly_fields(self, request: HttpRequest, obj=None):
        if obj:
            return self.readonly_fields + ("cpf", "role")
        return self.readonly_fields

    def get_fieldsets(self, request: HttpRequest, obj=None):
        if obj:
            if request.user.role == Role.INVESTOR:
                return self.fieldsets
            return self.fieldsets + (
                (
                    _("permissions"),
                    {
                        "fields": (
                            ("groups",),
                            ("user_permissions",),
                        )
                    },
                ),
                (_("metadata"), {"fields": ("date_joined", "last_login")}),
            )
        return self.add_fieldsets

    def save_model(self, request: request.HttpRequest, obj: User, form, change) -> None:
        if not change:
            obj.save()
            user_set_permissions(user=obj)
        obj.save()

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if request.user.role == Role.INVESTOR:
            return super().get_queryset(request).filter(id=request.user.id)
        return super().get_queryset(request)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return super().has_add_permission(request) and not request.user.role == Role.INVESTOR

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin):
    pass
