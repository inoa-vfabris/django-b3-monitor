import os
from pathlib import Path
from typing import Any, Dict, List

import environ
from django.utils.translation import gettext_lazy as _

# Build paths from src directory
BASE_DIR: Path = Path(__file__).resolve()
for x in range(10):
    BASE_DIR = BASE_DIR.parent
    if BASE_DIR.name == "src":
        break
else:
    raise AssertionError("Project not build from src directory")

ROOT_DIR: Path = BASE_DIR.parent

env: environ.Env = environ.Env()


SECRET_KEY: str = env("DJANGO_SECRET_KEY", default="django-insecure-foo-123")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
DEBUG: bool = env("DJANGO_DEBUG", cast=bool, default=False)
USE_DEBUG_TOOLBAR = env("USE_DEBUG_TOOLBAR", cast=bool, default=False)

SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", bool, default=False)
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", bool, default=False)
SECURE_HSTS_SECONDS = env("SECURE_HSTS_SECONDS", int, default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env("SECURE_HSTS_INCLUDE_SUBDOMAINS", bool, default=False)
SECURE_HSTS_PRELOAD = env("SECURE_HSTS_PRELOAD", bool, default=False)
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", bool, default=False)

# Security - CSRF
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=["http://*.com", "https://*.ngrok-free.app"]
)
LOGGING_LEVEL: str = env("DJANGO_LOGGING_LEVEL", default="INFO")
LOGGING = {
    "version": 1,
    "loggers": {
        "django.server": {
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "django.db.backends": {
            "level": "WARNING",
            "propagate": False,
        },
    },
}
# Password Validation
AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTH_USER_MODEL = "users.User"


# Application definition
INSTALLED_APPS = [
    "django_extensions",
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "corsheaders",
    "app.apps.RootAppConfig",
]


ADMIN_URL_PREFIX = "a"
LOGIN_URL = f"/{ADMIN_URL_PREFIX}/login/"
LOGIN_REDIRECT_URL: str = f"/{ADMIN_URL_PREFIX}/"

MIDDLEWARE: List[str] = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF: str = "app.urls"
TEMPLATES: List[Dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "app", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION: str = "app.wsgi.application"
ASGI_APPLICATION: str = "app.asgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": env("SQL_ENGINE", default="django.db.backends.postgresql"),
        "NAME": env("SQL_DATABASE", default="django-d3-monitor"),
        "USER": env("SQL_USER", default="postgres"),
        "PASSWORD": env("SQL_PASSWORD", default="postgres"),
        "HOST": env("SQL_HOST", default="localhost"),
        "PORT": env("SQL_PORT", default="5432"),
    }
}

# Internationalization
LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("pt-br", _("Brazilian Portuguese")),
    ("en-us", _("English")),
]
LOCALE_PATHS = [
    ROOT_DIR / "locale",
]
USE_I18N: bool = True

# Internationalization
# Dates
FORMAT_MODULE_PATH: List[str] = [
    "app.settings.formats",
]


# Time Zone
TIME_ZONE: str = "UTC"
USE_TZ: bool = True

# Static Files
STATIC_URL: str = "/static/"
STATIC_ROOT: str = os.path.join(ROOT_DIR, env("STATIC_ROOT", default="storage/static"))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, direc) for direc in env.list("STATICFILES_DIRS", default=[])
]
STATICFILES_FINDERS: List[str] = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Media files
MEDIA_ROOT = os.path.join(ROOT_DIR, env("MEDIA_ROOT", default="storage/media/"))
MEDIA_URL = "/media/"

# Storages
DEFAULT_FILE_STORAGE_BACKEND = env(
    "DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)
STATICFILES_STORAGE_BACKEND = env(
    "STATICFILES_STORAGE_BACKEND", default="django.contrib.staticfiles.storage.StaticFilesStorage"
)
PUBLIC_MEDIA_STORAGE_BACKEND = env(
    "PUBLIC_MEDIA_STORAGE_BACKEND", default=DEFAULT_FILE_STORAGE_BACKEND
)
STORAGES = {
    "default": {"BACKEND": DEFAULT_FILE_STORAGE_BACKEND},
    "staticfiles": {"BACKEND": STATICFILES_STORAGE_BACKEND},
    "public_media": {"BACKEND": PUBLIC_MEDIA_STORAGE_BACKEND},
}

REDIS_HOST = env("REDIS_HOST", default="redis")
REDIS_PORT = env.int("REDIS_PORT", default=6379)
REDIS_PASSWORD = env("REDIS_PASSWORD", default=None)
REDIS_DB = env("REDIS_DB", default="0")
if REDIS_PASSWORD is None:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
else:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

DEFAULT_QUEUE_NAME: str = env("DEFAULT_QUEUE_NAME", default="default")
CELERY_ACKS_LATE: bool = env("CELERY_ACKS_LATE", default=True)
CELERY_TRACK_STARTED: bool = env("CELERY_TRACK_STARTED", default=False)
CELERY_WORKER_PREFETCH_MULTIPLIER: int = env("CELERY_WORKER_PREFETCH_MULTIPLIER", default=1)
CELERY_ALWAYS_EAGER: bool = env("CELERY_ALWAYS_EAGER", default=False)
BROKER_URL = REDIS_URL

CORS_ORIGIN_ALLOW_ALL: bool = env.bool("CORS_ORIGIN_ALLOW_ALL", default=False)
if not CORS_ORIGIN_ALLOW_ALL:
    CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=[])

PROJECT_NAME = env.str("PROJECT_NAME")
HOST = env.str("HOST", default="localhost")

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")

EMAIL_HOST = env("EMAIL_HOST", default="mailpit")
EMAIL_PORT = env.int("EMAIL_PORT", default=1025)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)


EMAIL_SUBJECT_PREFIX = env("EMAIL_SUBJECT_PREFIX", default=f"[{PROJECT_NAME.title()}] -")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=f"{PROJECT_NAME.title()} <noreply@{HOST}>")
SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

JAZZMIN_SETTINGS = {
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "site_title": "Admin",
    "site_brand": "B3 Monitor",
    "site_header": "Admin",
    "welcome_sign": "B3 Monitor",
    "user_avatar": None,
    "show_sidebar": True,
    "navigation_expanded": True,
    # https://fontawesome.com/v5/search?m=free
    "icons": {},
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "show_ui_builder": False,
    "language_chooser": False,
}
JAZZMIN_UI_TWEAKS = {
    "actions_sticky_top": True,
    "navbar_fixed": True,
}
