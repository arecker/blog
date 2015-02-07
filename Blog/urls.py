from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'Blog.apps.Blogging.views.get_home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^feed/$', 'Blog.apps.Blogging.views.get_feed', name='feed'),
    url(r'^(?P<slug>[^/]+)/$', 'Blog.apps.Blogging.views.get_post', name='post'),
)
