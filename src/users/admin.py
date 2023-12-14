from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.utils.translation import gettext_lazy as _
from rest_framework import request
from rest_framework.authtoken.models import TokenProxy

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
        "full_name",
        "email",
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
                    "full_name",
                    "email",
                    "password",
                    "cpf",
                    "role",
                    "is_active",
                )
            },
        ),
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
    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("email", "cpf", "role", "password1", "password2")},
        ),
    )
    readonly_fields = ("date_joined", "last_login")
    search_fields = ("email", "full_name", "cpf")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")
    show_full_result_count = False

    def save_model(self, request: request.HttpRequest, obj: User, form, change) -> None:
        if not change:
            obj.save()
            user_set_permissions(user=obj)
        obj.save()


@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin):
    pass
