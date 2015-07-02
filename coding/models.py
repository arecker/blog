from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=200, blank=True, null=True)
    image = models.ImageField(
        upload_to='coding/project',
        null=True,
        blank=True
    )
    url = models.URLField(verbose_name='URL', blank=True, null=True)
    added = models.DateField(default=timezone.now)
    repo = models.URLField(verbose_name='Repository', blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-added']
