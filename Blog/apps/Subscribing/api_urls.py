from django.conf.urls import patterns, url

urlpatterns = patterns('Blog.apps.Subscribing.api_views',
    url(r'^subscribe/', 'subscriber_add'),
    url(r'^unsubscribe/', 'subscriber_remove'),
)