from .base import *

ALLOWED_HOSTS = ['3.39.12.91', 'www.neworld.kr', 'neworld.kr']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = False

STATICFILES_DIRS = [
    '/projects/mysite/static/img/',
]
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'neworld',
#         'USER': 'dbmaster',
#         'PASSWORD': 'WTmZdaBclaNrvZVLcfol',
#         'HOST': 'databasecamp.cjo3f5o7oksd.ap-northeast-2.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }
