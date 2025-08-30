"""
Configuración para desarrollo local
"""
from .base import *

# Crear directorio de logs si no existe
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/staticfiles/"
STATIC_ROOT = BASE_DIR / 'staticfiles'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c8+r+zx31n2lley-am@-4s&6p=(8_336*^i6vzjajt73kpg!16'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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
