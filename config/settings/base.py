"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.
# import neworld

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm(1kae9!%=wcde_xsgpr+walb^zsa(*fs-mx6-09twf*_)l539'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['3.37.207.152']


# Application definition

INSTALLED_APPS = [
    'common.apps.CommonConfig',
    'neworld.apps.NeworldConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'six',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# ????????? ????????? ???????????? URL
LOGIN_REDIRECT_URL = '/'

# ??????????????? ???????????? URL
LOGOUT_REDIRECT_URL = '/'

# ????????????
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/mysite.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'neworld': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_BACKEND = 'django_ses.SESBackend'

'''
# These are optional -- if they're set as environment variables they won't
# need to be set here as well
AWS_ACCESS_KEY_ID = 'ubuntu'
AWS_SECRET_ACCESS_KEY = '-----BEGIN RSA PRIVATE KEY-----\
MIIEpAIBAAKCAQEAyFkcgO5OGgXmWnbblW93pCHrFLIdnbXgVIiKkmYNypRjYXXq\
s7OxvS745af8fiBktoOORWZNsxDzYj2LC35IZauJlsyvzBIY7yLEKbzzZMTJj5jA\
fdO1YlBJizSietOE3osBPyz2GIciND1c4QKGwomTNiI2hOJ7XUiSjgHIDUtValLN\
zSQ5nRIiE4vxU3r7IGeL4L6199vXK5I2CgSkCIJsv3wT/rIoKANwDh1mw3U8+Y6e\
Y1TdvbniDXjr2gu5ez1XQLICWCFv5kj+UMjs+5QXNOlMectatFGL/EM23sOX9g4B\
2WWRIhIbDDFGERBHAyv5P8jCGpQdmqx/DmcE8wIDAQABAoIBAQCUppmhiC9m243I\
/Xt7axNIMuprlqSmybXCwvSeHx6IeoUqYQVdhCySg/Gk5HlRU9OmIAJFt9xaym7r\
K2Kpim9JEHer7f9Z2OurMw59MXceA2zSILJiKdzhL1UB9nG/1IU3YcfxCfkmxc05\
GXZ6dRdr7AvQFJ6DBlAmLJygxO2b/kG/VCBG2S82VI5Np6/fC12r8qLHezB6PSip\
mb47AAuDVXKqZ0iwXkSrB0Q5T9e6QCwwWd2IzVCy68m+yCHUOdav3ggTD6UDjg40\
Qb35CFxfGgjom3Bj03q4zbZ3NV+7AvkjxCtIXtI+vm5gIzAl3d5WKRQhbq8cuS+5\
uj8mbOghAoGBAPib67gJne8tSj0o7aGKA6Wbd+KIMgpzYKtsSarL2SMW98925Uzd\
Wg5PDhjEMB6Zp2t2Q+BgoX8mBHyYgkNTiKazrXzw3AU+lnSWxKf4Zn1Z5TVkWF9Q\
t9MnyIm2xgSMsKRG4mAOCLCA1por+oc3ShcLitU/6EuOmd5AHhM4FunpAoGBAM5N\
5IXwNBPKuVmPOUZJIMIMgqsdPOOsa72bMnmtDZOa08W03M2DSypceGHzs6OGpEnR\
g6IFIONK78HJJXKPhuFTIpnALMrOKF12qlNyEwmSzZM4ZOiS0r1SIxwVpQDJ3Nnv\
pTATGUPpzsLOv3pk0xsWY4V3jI/3vmrYfMpduFJ7AoGAKMCucDmrWQSskb/+zCcq\
l+AXU9wNj+b/5rnWjZfi3TyrnKeZyPLUC1psLiUi2jFH33bAg6xzbLtXqvD5EX5E\
/Uag3sVA2985nJ0GWZ5/dnbg+tKbJey+ZW+1ENYUObSyVAuGmkZSqFRGWXlyFO48\
R/DNbk2Oj6wtjuAlzfK41tkCgYA10D2m7mQ3MW8tvF1dRyADXg4LooHKhaRI/h2p\
fYmIEh/hd28NMI0/zIUeT9pw8mMSWlNyxNGyWE64Bsb83hF53xysbGOCt0nyL0z4\
nU339lInb9NqkznjZnSAE+lJjl5MfuVg5+p0O53SVOm/fGNQsoNdQjTpLN9/sV7D\
zrSQ1wKBgQDIbP5+dyWQj1rOVrLXU+mGaZp1svXGmi0/kFqfi+xs5aoZkgEn1WpM\
a0RMqmKugwdY78YLKYwLRt/cWaYzRX1JbH56it1Y2AnBo5AfN9VKEJcAu6Zfw//J\
Y6cbqb32hEQbJAOtsX/2n0sv9iTStF/QXNhtqBNF6TPKU+4yNd1WXw==\
-----END RSA PRIVATE KEY-----'

# Additionally, if you are not using the default AWS region of us-east-1,
# you need to specify a region, like so:
AWS_SES_REGION_NAME = 'ap-northeast-2'
AWS_SES_REGION_ENDPOINT = 'email.ap-northeast-2.amazonaws.com'
'''

# CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'


# EMAIL_HOST = 'smtp.gmail.com'
# # ????????? ??????????????? ??????
# EMAIL_PORT = '587'
# # gmail?????? ???????????? ??????
# EMAIL_HOST_USER = 'neworld0@gmail.com'
# # ????????? ?????????
# EMAIL_HOST_PASSWORD = '2tjdudEgjs!'
# # ????????? ????????? ????????????
# EMAIL_USE_TLS = True
# # TLS ?????? ??????
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# # ???????????? ????????? ??????????????? ?????? ????????? ??????,'webmaster@localhost'



