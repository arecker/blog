from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from api import ROUTER
from content.views import random_image
from subscribing.views import unsubscribe, verify, NewSubscriberView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(ROUTER.urls)),

    url(r'^subscribe/$', NewSubscriberView.as_view()),
    url(r'^verify/(?P<key>[^/]+)/$', verify, name='verify'),
    url(r'^unsubscribe/(?P<key>[^/]+)/$', unsubscribe, name='unsubscribe'),

    url(r'^random-image/$', random_image, name='random-image'),

]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
