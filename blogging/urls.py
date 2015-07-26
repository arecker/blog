from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^feed/$', views.view_post_feed),
    # url(r'^(?P<slug>[^/]+)/$', views.view_post, name='view_blog_post')
    url(
        r'^(?P<slug>[^/]+)/$',
        views.PostDetailView.as_view(),
        name='view_blog_post'
    )
]
