from os.path import dirname, join, abspath


BASE_DIR = dirname(dirname(dirname(abspath(__file__))))

INSTALLED_APPS = ['django.contrib.admin',  # Django Apps
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',

                  'sorl.thumbnail',  # 3rd Party Apps
                  'rest_framework',

                  'content',    # Project Apps
                  'subscribing']

MIDDLEWARE_CLASSES = ['django.middleware.security.SecurityMiddleware',
                      'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware',
                      'django.middleware.clickjacking.XFrameOptionsMiddleware']

ROOT_URLCONF = 'blog.urls'
WSGI_APPLICATION = 'blog.wsgi.application'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(BASE_DIR, 'templates')],
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# protocol, domain, no trailing slash
URL_BASE = 'https://backend.alexrecker.com'
