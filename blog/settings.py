import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'swiggity swooty'
DEBUG = True
ALLOWED_HOSTS = ['*',]

INSTALLED_APPS = (
    # Django Admin Extensions
    'flat',

    # Defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Other Extensions
    'djangobower',
    'compressor',
    'epiceditor',
    'rest_framework',
    'django_nose',

    # Apps
    'blogging',
    'subscribing',
    'home'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'blog.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'blog.wsgi.application'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'temp', 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    )
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'prod_static')
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'djangobower.finders.BowerFinder',
    'compressor.finders.CompressorFinder',
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'bower')
BOWER_INSTALLED_APPS = (
    'angular',
    'angular-route',
    'angular-mocks',
    'bootswatch-dist#sandstone',
    'barberboy/vollkorn',
    'fontawesome'
)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'temp')
EMAIL_FROM = 'alex@reckerfamily.com'


try:
    from prod_settings import *
except ImportError:
    pass
