from django.db import models


class Post(models.Model):
    title = models.CharField(verbose_name='Title', max_length=120)
    slug = models.SlugField(verbose_name='Slug', max_length=120, unique=True)
    date = models.DateField(verbose_name='Date', auto_created=True, db_index=True)
    published = models.BooleanField(verbose_name='Publish', default=False)
    body = models.TextField(verbose_name='Body', blank=True, null=True)

