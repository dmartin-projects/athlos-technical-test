"""
Configuración para producción
"""
import os
from .base import *

# SECURITY: Use environment variable for secret key, fallback to base.py for build
SECRET_KEY = os.getenv('SECRET_KEY') or SECRET_KEY

# Security settings for production
DEBUG = False

# Static files (CSS, JavaScript, Images)
# STATIC_URL = "/staticfiles/"
# STATIC_ROOT = '/tmp/staticfiles'
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

# Security settings
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_SECONDS = 86400
# SECURE_REDIRECT_EXEMPT = []
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# CORS settings for production
CORS_ALLOW_ALL_ORIGINS = True