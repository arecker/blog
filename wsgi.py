import os, sys
sys.path.append('/home/alex/Django/Blog/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Blog.settings'
activate_this = "/home/alex/Django/Blog/env/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()