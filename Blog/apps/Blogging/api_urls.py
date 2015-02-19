from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'Blog.apps.Blogging.views.get_archives', name='home'),
)