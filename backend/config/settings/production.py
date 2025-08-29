"""
Configuración para producción
"""
import os
from .base import *

LOGS_DIR = Path(os.environ.get("LOGS_DIR", "/tmp/logs"))


# SECURITY: Use environment variable for secret key
SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required for production")

# Security settings for production
DEBUG = False

ALLOWED_HOSTS = [
    os.getenv('DOMAIN_NAME', ''),
    f"api.{os.getenv('DOMAIN_NAME', '')}",
    os.getenv('SERVER_IP', ''),
]

# Database para producción postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 86400
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS settings for production
CORS_ALLOW_ALL_ORIGINS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s %(process)d %(thread)d [%(pathname)s/%(module)s.%(funcName)s:%(lineno)s] %(message)s"
            },    
        },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        }
    },
    "handlers": {
        "debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "debug.log",
            "formatter": "verbose",
        },
        "info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "info.log",
            "formatter": "verbose",
        },
        "warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "warning.log",
            "formatter": "verbose",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "error.log",
            "formatter": "verbose",
        },
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {        
        "django": {
            "handlers": ["debug", "info", "warning", "error", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
