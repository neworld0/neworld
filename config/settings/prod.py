from .base import *

ALLOWED_HOSTS = ['3.39.12.91', 'www.neworld.kr', 'neworld.kr']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = False

STATICFILES_DIRS = [
    '/projects/mysite/static/img/',
]
