from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.base import AutoTimeStampModel


class B3Stock(AutoTimeStampModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
    )
    code = models.CharField(
        verbose_name=_("Code"),
        max_length=10,
    )

    class Meta:
        verbose_name = _("B3 stock")
        verbose_name_plural = _("B3 stocks")

    def __str__(self):
        return f"{self.name}-{self.code}"


class B3StockPrice(AutoTimeStampModel):
    B3_monitored_stock = models.ForeignKey(
        verbose_name=_("B3 monitored stock"),
        to="stocks.MonitoredStock",
        on_delete=models.CASCADE,
        related_name="B3_monitored_stocks",
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        verbose_name = _("B3 stock price")
        verbose_name_plural = _("B3 stock prices")

    def __str__(self):
        return self.B3_monitored_stock.B3_stock.name


class MonitoredStock(AutoTimeStampModel):
    B3_stock = models.ForeignKey(
        verbose_name=_("B3 stock"),
        to="stocks.B3Stock",
        on_delete=models.CASCADE,
        related_name="monitored_stocks",
    )
    user = models.ForeignKey(
        verbose_name=_("User"),
        to="users.User",
        on_delete=models.CASCADE,
        related_name="monitored_stocks",
    )
    check_periodicity = models.PositiveSmallIntegerField(
        verbose_name=_("Check periodicity"),
        help_text=_("The time, in minutes, that the stock will be checked."),
        default=1,
    )
    superior_limit = models.PositiveSmallIntegerField(
        verbose_name=_("Superior limit"),
    )
    inferior_limit = models.PositiveSmallIntegerField(
        verbose_name=_("Inferior limit"),
    )

    class Meta:
        verbose_name = _("Monitored stock")
        verbose_name_plural = _("Monitored stocks")

    def __str__(self):
        return f"{self.user.email}-{self.B3_stock.code}"

    def clean_valid_data(self) -> None:
        if self.check_periodicity == 0:
            raise ValidationError(_("Check periodicity must be greater than 0."))
        if self.superior_limit <= self.inferior_limit:
            raise ValidationError(_("Superior limit must be greater than inferior limit."))
