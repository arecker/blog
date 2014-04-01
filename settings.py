#region Settings
#region Imports
SECRET_KEY = 'kt26*9sry8sl&s(#vq!hxr4z-0d2-=1=r0sa!2b^vn69q-&oiu'
import os
from django.shortcuts import render_to_response
from django.conf.urls import patterns
from django.http import HttpResponse
from os.path import join as Join
import markdown2, BeautifulSoup
filepath, extension = os.path.splitext(__file__)
#endregion

#region Deployment
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []
WSGI_APPLICATION = 'wsgi.application'
ROOT_URLCONF = os.path.basename(filepath)
PAGES = os.path.abspath(Join(filepath, '..', 'pages'))
#endregion

#region Locale
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
#endregion

#region Static Files
STATIC_ROOT = Join(filepath, '..', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    Join(STATIC_ROOT, "libs"),
    Join(STATIC_ROOT, "css"),
    Join(STATIC_ROOT, "img"),
)
#endregion

#region Middleware
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
#endregion

#region Logging
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
#endregion

#region Templates
TEMPLATE_DIRS = (
    (Join(filepath, '..', 'templates')),
)
#endregion
#endregion

# Models
class Post:
    def __init__(self, meta_title="Meta Title", meta_description="meta description", meta_canonical="Meta Canonical", title='Title', body='Body'):
        self.Meta_title = meta_title
        self.Meta_description = meta_description
        self.Meta_canonical=meta_canonical
        self.Title = title
        self.Body = body


# Controllers
def GetHome(request):
    for _meta_title, _meta_description, _meta_canonical in GetMetaFromMD(Join(PAGES, 'home.md')):
        meta_title = _meta_title
        meta_description = _meta_description
        meta_canonical = _meta_canonical

    body = GetBodyFromMD(Join(PAGES, 'home.md'))
    post = Post(title="Blog by Alex Recker", body=body)
    return render_to_response('base.html', {
        'post': post,
    })

def GetArchives(request):
    post = Post(title="Archives Page", body="Archives Body")
    return render_to_response('base.html', {
        'post': post,
    })

def GetProjects(request):
    post = Post(title="Projects Page", body="Projects Body")
    return render_to_response('base.html', {
        'post': post,
    })

def GetFriends(request):
    for _meta_title, _meta_description, _meta_canonical in GetMetaFromMD(Join(PAGES, 'friends.md')):
        meta_title = _meta_title
        meta_description = _meta_description
        meta_canonical = _meta_canonical

    body = GetBodyFromMD(Join(PAGES, 'friends.md'))

    post = Post(meta_title, meta_description, meta_canonical, title="Friends Page", body=body)
    return render_to_response('base.html', {
        'post': post,
    })

def GetPost(request, slug):
    return HttpResponse(slug)

# Helpers
def GetMetaFromMD(PATH):
    soup = BeautifulSoup.BeautifulSoup(markdown2.markdown_path(PATH))
    metadata = []
    for h3 in soup.findAll('h3'):
        metadata.append(h3.string)
    return (metadata,)

def GetBodyFromMD(PATH):
    return markdown2.markdown_path(PATH).split('[ end metadata ]')[-1]


# Routes
urlpatterns = patterns('',
    (r'^$', GetHome),
    (r'^archives/', GetArchives),
    (r'^projects/', GetProjects),
    (r'^friends/', GetFriends),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve'),
    (r'^(?P<slug>[^/]+)', GetPost),
)