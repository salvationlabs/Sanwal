from decouple import config
import dj_database_url

from .base import *

ALLOWED_HOSTS = ['.sanwal.org']

## CSRF TOKEN CLEARANCE
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = '.sanwal.org'
CSRF_TRUSTED_ORIGINS = ['https://sanwal.org', 'https://www.sanwal.org']

## Secure-Only Session Cookie
SESSION_COOKIE_SECURE = True

# POSTGRESQL Database setup
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

# AWS S3 Storage
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = F'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read'

AWS_LOCATION = 'static'

# Media
DEFAULT_FILE_STORAGE = 'core.storages.MediaStore'

# Static Configuration S3
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
