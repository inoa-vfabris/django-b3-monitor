from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class MyAdminConfig(AdminConfig):
    default_site = "app.admin.site.MyAdminSite"

class RootAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
