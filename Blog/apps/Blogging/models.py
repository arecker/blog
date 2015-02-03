from django.db import models
import slugify


class Post(models.Model):
    title = models.CharField(verbose_name='Title', max_length=120)
    slug = models.SlugField(verbose_name='Slug', max_length=120, unique=True, blank=True)
    date = models.DateField(verbose_name='Date', auto_created=True, db_index=True)
    published = models.BooleanField(verbose_name='Publish', default=False)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    body = models.TextField(verbose_name='Body', blank=True, null=True)


    def save(self, *args, **kwargs):
        # Extend save function to slugify title
        self.slug = slugify.slugify(self.title, to_lower=True)
        return super(Post, self).save(*args, **kwargs)


    def get_truncated_description(self, length=50, suffix='...'):
        if len(self.description) <= length:
            return self.description
        else:
            return ' '.join(self.description[:length+1].split(' ')[0:-1]) + suffix
    get_truncated_description.short_description = 'Description'


    def __unicode__(self):
        return self.title