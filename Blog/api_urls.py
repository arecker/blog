from django.conf.urls import patterns, url, include

urlpatterns = patterns('Blog.apps.Subscribing.views',
    url(r'^subscriber/', include('Blog.apps.Subscribing.urls')),
    url(r'^blog/', include('Blog.apps.Blogging.api_urls')),
)