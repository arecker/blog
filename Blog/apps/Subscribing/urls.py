from django.conf.urls import patterns, url

urlpatterns = patterns('Blog.apps.Subscribing.views',
    url(r'^subscriber/', 'subscriber_add'),
    url(r'^unsubscriber/', 'subscriber_remove'),
)