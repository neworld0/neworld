import environ

from .base import *

ALLOWED_HOSTS = ['3.39.12.91', 'neworld.kr', 'www.neworld.kr']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

# Production-only settings must never inherit the development defaults in
# base.py.  DJANGO_SECRET_KEY is deliberately required so a deployment fails
# safely if the server has not been configured with a real secret.
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env.bool('DJANGO_DEBUG', default=False)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '5432',
    }
}
