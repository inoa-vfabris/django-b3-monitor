from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from users.consts import Role
from users.models import User


def user_set_permissions(user: User):
    if user.role == Role.ADMIN:
        user.is_superuser = True
    if user.role == Role.INVESTOR:
        content_types = ContentType.objects.filter(app_label="stocks")
        permissions = Permission.objects.filter(content_type__in=content_types)
        user.user_permissions.set(objs=permissions)
    user.is_staff = True
    user.save()
