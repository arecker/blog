from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^subscribing/', include('Blog.apps.Subscribing.api_urls')),
    url(r'^blogging/', include('Blog.apps.Blogging.api_urls')),
)