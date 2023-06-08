import dj_database_url

from .base import *

ALLOWED_HOSTS = ['.sanwal.org']

## CSRF TOKEN CLEARANCE
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = '.sanwal.org'
CSRF_TRUSTED_ORIGINS = ['https://sanwal.org', 'https://www.sanwal.org']

## Secure-Only Session Cookie
SESSION_COOKIE_SECURE = True

DATABASE_URL = os.getenv("DATABASE_URL")

DATABASES = {
    #       POSTGRESQL CONNECTION ONE WAY

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': os.getenv("DB_NAME"),
    #     'USER': os.getenv("DB_USER"),
    #     'PASSWORD': os.getenv("DB_PASSWORD"),
    #     'HOST': os.getenv("DB_HOST"),
    #     'PORT': os.getenv("DB_PORT"),
    # }

    #       POSTGRESQL CONNECTION ANOTHER WAY

    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}