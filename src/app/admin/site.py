from django.contrib import admin

from stocks import models
from users import consts
from users.models import User


class MyAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        """Overrides the default `index` method, to add custom extra content to the admin index page"""
        numbers_of_investors = User.objects.filter(role=consts.Role.INVESTOR).count()
        extra_context = {
            "is_admin": request.user.role == consts.Role.ADMIN,
            "numbers_of_stocks": models.B3Stock.objects.count(),
            "number_of_monitored_stocks": models.MonitoredStock.objects.count(),
            "numbers_of_investors": numbers_of_investors,
            "my_stocks": models.MonitoredStock.objects.filter(user=request.user).count(),
        }
        return super().index(request, extra_context=extra_context)
