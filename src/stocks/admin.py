from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from app.admin.mixins import ReadOnlyAdminMixin
from users.consts import Role

from . import models, services


@admin.register(models.B3Stock)
class B3StockAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = [
        "name",
        "code",
    ]
    search_fields = [
        "name",
        "code",
    ]
    show_full_result_count = False


class B3StockPriceInline(admin.TabularInline):
    model = models.B3StockPrice
    readonly_fields = ["price", "last_updated_at"]


@admin.register(models.MonitoredStock)
class MonitoredStockAdmin(admin.ModelAdmin):
    inlines = [
        B3StockPriceInline,
    ]
    list_display = [
        "user",
        "B3_stock",
        "check_periodicity",
        "superior_limit",
        "inferior_limit",
    ]
    show_full_result_count = False
    exclude = ("user",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[models.MonitoredStock]:
        if request.user.role==Role.INVESTOR:
            return super().get_queryset(request).filter(user=request.user)
        return super().get_queryset(request)

    def save_model(
        self, request: HttpRequest, obj: models.MonitoredStock, form, change: bool
    ) -> None:
        if not change:
            obj.user = request.user
            scheduler = BackgroundScheduler()
            scheduler.add_job(
                services.stock_limit_monitor,
                "interval",
                seconds=timedelta(minutes=obj.check_periodicity).total_seconds(),
                args=[obj],
            )
            scheduler.start()
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return super().has_add_permission(request) and request.user.role == Role.INVESTOR

    def has_delete_permission(
        self, request: HttpRequest, obj=None
    ) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj=None
    ) -> bool:
        return False
