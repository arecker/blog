from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'never'
    priority = 1

    def items(self):
        return Post.objects.published()

    def lastmod(self, obj):
        return obj.date
