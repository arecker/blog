from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name="writing/home.html"),
        name='home'
    ),
    url(
        r'^archives/$',
        views.PostListView.as_view(),
        name='post-list'
    ),
    url(
        r'^(?P<slug>[^/]+)/$',
        views.PostDetailView.as_view(),
        name='post-detail'
    )
]
