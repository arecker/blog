from .common import *


SECRET_KEY = 'thats-so-raven'
DEBUG=True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'temp/db.sqlite3'),
    }
}

MEDIA_ROOT = join(BASE_DIR, 'temp/uploads')
STATIC_ROOT = join(BASE_DIR, 'temp/static')

AUTH_PASSWORD_VALIDATORS = []
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = join(BASE_DIR, 'temp/email')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    )
}

CORS_ORIGIN_ALLOW_ALL = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(BASE_DIR, 'temp/debug.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG'
        },
    }
}

URL_BASE = 'http://localhost:8000'
