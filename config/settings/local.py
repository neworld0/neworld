from .base import *

ALLOWED_HOSTS = []

STATICFILES_DIRS = [
    BASE_DIR / 'static',
    '/projects/mysite/static/img/',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '2tjdudEgjs!',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
