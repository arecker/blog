from django.conf.urls import url

from . import views


urlpatterns = [
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
