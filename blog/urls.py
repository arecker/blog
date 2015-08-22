from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.views.generic import TemplateView

from blog.sitemap import sitemap_sections


urlpatterns = [
    url(
        r'^robots\.txt$',
        TemplateView.as_view(
            template_name='robots.txt',
            content_type='text/plain'
        ),
    ),

    url(
        r'^sitemap\.xml$',
        sitemap_view,
        {'sitemaps': sitemap_sections},
        name='django.contrib.sitemaps.views.sitemap'
    ),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^subscribe/', include('subscribing.urls')),
    url(r'^', include('writing.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
