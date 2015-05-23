from django.db import models
from django.db.models import permalink


class Post(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    date = models.DateField(auto_now=True)
    published = models.BooleanField(default=False)
    description = models.TextField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    image_url = models.URLField(verbose_name='Image URL', blank=True, null=True)


    def __unicode__(self):
        return self.title


    @permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, { 'slug': self.slug })