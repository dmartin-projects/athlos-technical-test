"""
Configuración para producción
"""
import os
from .base import *

# SECURITY: Use environment variable for secret key, fallback to base.py for build
SECRET_KEY = os.getenv('SECRET_KEY') or SECRET_KEY

# Security settings for production
DEBUG = False


STATIC_URL = "/staticfiles/"
STATIC_ROOT = BASE_DIR / '/staticfiles'

ALLOWED_HOSTS = ['*']

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


# CORS settings for production
CORS_ALLOW_ALL_ORIGINS = True

# Override SPECTACULAR_SETTINGS for production
SPECTACULAR_SETTINGS = {
    'TITLE': 'Scrapper API',
    'DESCRIPTION': 'API para scrapping de datos',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/v1/',
    'SWAGGER_UI_SETTINGS': {
        'url': '/api/v1/schema/',
        'supportedSubmitMethods': ['get', 'post', 'put', 'patch', 'delete']
    }
}