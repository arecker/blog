from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .api import router
from home.views import HomeIndexView
from django.views.generic import TemplateView
from subscribing.views import get_unsubscribe_view


urlpatterns = [
    url(
        r'^robots\.txt$',
        TemplateView.as_view(template_name='robots.txt'),
    ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^unsubscribe/(?P<key>[^/]+)/$', get_unsubscribe_view),
    url(r'^$', HomeIndexView.as_view()),
    url(r'^', include('blogging.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
