logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "gunicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
access_log_format = " ".join(
    [
        "%({x-forwarded-for}i)s",
        "%({x-request-id}i)s",
        "%(s)s",
        "%(m)s",
        "%(U)s?%(q)s",
        "%(M)sms",
        "'%({authorization}i)s'",
        "'%(a)s'",
    ]
)
