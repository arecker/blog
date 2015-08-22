from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(
        r'^$',
        views.subscribe,
        name='subscribe'
    ),
    url(
        r'^thanks/$',
        TemplateView.as_view(template_name='subscribing/thanks.html'),
        name='subscribe-thanks'
    ),
    url(
        r'^verify/(?P<key>[^/]+)/$',
        views.verify,
        name='verify'
    ),
    url(
        r'^unsubscribe/(?P<key>[^/]+)/$',
        views.unsubscribe,
        name='unsubscribe'
    )
]
