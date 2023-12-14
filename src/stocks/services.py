from datetime import datetime
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from users.models import User

from . import models


def stock_limit_monitor(obj: models.MonitoredStock):
    print("checking price")
    stock = obj.B3_stock
    url = "https://www.dadosdemercado.com.br/bolsa/acoes"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "stocks"})
    lines = table.tbody.find_all("tr")
    for line in lines:
        if line.find("td").strong.a.text == stock.code:
            price = Decimal(
                line.find_all("td", {"class": "right"})[1].text.replace(".", ",").replace(",", ".")
            )
            models.B3StockPrice.objects.create(B3_monitored_stock=obj, price=price)
            break
    if obj.superior_limit < price:
        limit_type = "superior"
        action = "venda"
    if obj.inferior_limit > price:
        limit_type = "inferior"
        action = "compra"
    else:
        return
    send_monitoring_email(user=obj.user, stock_code=stock.code, limit_type=limit_type, action=action, price=price, limit=obj.limit, date=datetime.now())
        


def send_monitoring_email(user: User, stock_code:str, limit_type:str, action:str,  price: Decimal, limit: Decimal, date:datetime):
    context = {
        "code": stock_code,
        "limit_type": limit_type,
        "action": action,
        "price": price,
        "limit": limit,
        "date": date,
    }
    send_mail(
        subject=_("Alert to your stock monitoring"),
        message=render_to_string("email/stock_monitoring.txt", context=context),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=user.email,
        html_message=render_to_string("email/stock_monitoring.html", context=context),
    )
