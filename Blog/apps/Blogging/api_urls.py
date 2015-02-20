from django.conf.urls import patterns, url

urlpatterns = patterns('Blog.apps.Blogging.api_views.',
    url(r'^post/$', 'get_posts', name='home'),
)