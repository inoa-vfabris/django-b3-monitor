import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.conf")

app = Celery("app")

CELERY_CONFIG = {
    "task_serializer": "json",
    "accept_content": [
        "json",
    ],
    "result_serializer": "json",
    "result_backend": None,
    "enable_utc": True,
    "enable_remote_control": False,
    "default_queue": settings.DEFAULT_QUEUE_NAME,
    "acks_late": settings.CELERY_ACKS_LATE,
    "track_started": settings.CELERY_TRACK_STARTED,
    "prefetch_multiplier": settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
    "task_always_eager": settings.CELERY_ALWAYS_EAGER,
    "broker_url": settings.BROKER_URL,
    "broker_connection_retry_on_startup": True,
    "beat_schedule": {
        "populate_b3_stocks_dados_mercado": {
            "task": "stocks.tasks.populate_b3_stocks_dados_mercado",
            "args": (),
            # https://crontab.guru/
            "schedule": crontab(
                hour=4,  # UTC (00h on America/Sao_Paulo)
                minute=0,
                day_of_week="mon-fri",
            ),
        }
    },
}

app.autodiscover_tasks(["stocks"])

app.conf.update(**CELERY_CONFIG)
