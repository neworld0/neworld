from .base import *
import os

ALLOWED_HOSTS = ['3.39.12.91']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]