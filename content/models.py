from __future__ import unicode_literals

from os.path import basename

from django.db import models
from django.utils.html import format_html
from sorl.thumbnail import ImageField, get_thumbnail

from blog.utils import get_uuid_pk


class BaseQuerySet(models.QuerySet):
    def slug(self, slug):
        return self.get(slug=slug)

    def pluck(self):
        return (self
                .filter(in_random=True)
                .order_by('?').first())


class BaseModel(models.Model):
    objects = BaseQuerySet.as_manager()

    id = get_uuid_pk()
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    in_random = models.BooleanField(default=True,
                                    verbose_name='Include in random')

    class Meta:
        abstract = True


class Document(BaseModel):
    file = models.FileField(upload_to='documents')

    def get_absolute_url(self):
        return self.file.url

    @property
    def filename(self):
        return basename(self.file.name)

    def __unicode__(self):
        return self.filename


class Image(BaseModel):
    file = ImageField(upload_to='images')

    @property
    def thumbnail(self):
        t = get_thumbnail(self.file, "100x100")
        return format_html('<img src="{}" />', t.url)

    def __unicode__(self):
        return self.name


class FortuneCookie(BaseModel):
    text = models.TextField()

    @property
    def truncated_text(self):
        words = self.text.split(' ')[:5]
        return ' '.join(words) + '...'

    def __unicode__(self):
        return self.truncated_text
