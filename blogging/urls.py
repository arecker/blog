from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^feed/$', views.view_post_feed),
    url(r'^(?P<slug>[^/]+)/$', views.view_post)
]
