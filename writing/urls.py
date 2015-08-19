from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^(?P<slug>[^/]+)/$',
        views.PostDetailView.as_view(),
        name='post-detail'
    )
]
