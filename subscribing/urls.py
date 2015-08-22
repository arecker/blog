from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(
        r'^subscribe/$',
        views.subscribe,
        name='subscribe'
    ),
    url(
        r'^subscribe/thanks/$',
        TemplateView.as_view(template_name='subscribing/thanks.html'),
        name='subscribe-thanks'
    ),
    url(
        r'^subscribe/verify/(?P<key>[^/]+)/$',
        views.verify,
        name='verify'
    )
]
