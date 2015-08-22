from django.db import models

from uuid import uuid4


class PhotoQuerySet(models.QuerySet):
    def enabled(self):
        return self.filter(enabled=True)

    def random(self):
        try:
            return self.order_by('?').first()
        except:
            return None


class Photo(models.Model):
    objects = PhotoQuerySet.as_manager()
    uuid = models.UUIDField(default=uuid4, editable=False)
    enabled = models.BooleanField(default=True)
    image = models.ImageField(upload_to='headers/')

    def __unicode__(self):
        return self.image.name
