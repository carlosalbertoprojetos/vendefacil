"""
Development settings for VendaSimples project.
"""

from .base import *

# Debug settings
DEBUG = True

# Development apps
# INSTALLED_APPS += [
#     'debug_toolbar',
# ]

# Development middleware
# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ]

# Database for development (SQLite for simplicity)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db_new.sqlite3",
    }
}

# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Debug toolbar settings
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

# Development-specific settings
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Disable autoreload debug messages
import logging

logging.getLogger("django.utils.autoreload").setLevel(logging.ERROR)

# Logging for development
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.utils.autoreload": {
            "handlers": [],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Cache settings for development (use local memory)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Session settings for development
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Media files served by Django in development
if DEBUG:
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

# Cart configuration
CART_SESSION_ID = "vendasimples_cart"
CART_SESSION_EXPIRE = 86400  # 24 hours

# Additional development settings
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
]

# Email settings for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# File upload settings for development
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Product settings
PRODUCT_IMAGE_MAX_SIZE = 5 * 1024 * 1024  # 5MB
PRODUCT_IMAGE_ALLOWED_FORMATS = ["jpg", "jpeg", "png", "gif", "webp"]

# Order settings
ORDER_NUMBER_PREFIX = "DEV"
ORDER_AUTO_CONFIRM = True
ORDER_CANCELLATION_HOURS = 24

# Notification settings
NOTIFICATION_EMAIL_ENABLED = True
NOTIFICATION_SMS_ENABLED = False
NOTIFICATION_WHATSAPP_ENABLED = True
NOTIFICATION_PUSH_ENABLED = False
