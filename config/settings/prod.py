from .base import *

ALLOWED_HOSTS = ['3.37.207.152', 'www.neworld.kr', 'neworld.kr']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = True

STATICFILES_DIRS = [
    '/projects/mysite/static/img/',
]
