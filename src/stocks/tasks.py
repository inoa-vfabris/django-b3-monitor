import requests
from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger

from src.app.celery.decorators import BaseTask, task

from . import models

logger = get_task_logger(__name__)


@task(bind=True)
def populate_b3_stocks_dados_mercado(self: BaseTask):
    url = "https://www.dadosdemercado.com.br/bolsa/acoes"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "stocks"})
    lines = table.tbody.find_all("tr")
    for line in lines:
        code = line.find("td").strong.a.text
        name = line.find_all("td")[1].text
        stock = models.B3Stock.objects.filter(code=code).first()
        if not stock:
            stock = models.B3Stock.objects.create(name=name, code=code)
    logger.info("B3 stocks populated successfully.")
