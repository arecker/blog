from django.db import models
from Blog.apps.Blogging.models import Post
from uuid import uuid1
import datetime


class Subscriber(models.Model):
    email = models.CharField(max_length=200, blank=None, unique=True, null=False)
    full_text = models.BooleanField(default=False)
    unsubscribe_key = models.CharField(max_length=150, blank=True)
    subscribe_date = models.DateField(verbose_name='Date', default=datetime.datetime.now())


    def save(self, *args, **kwargs):
        # Extend save function to slugify title
        if not self.unsubscribe_key:
            self.unsubscribe_key = str(uuid1().hex)
        return super(Subscriber, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.email



class Newsletter(models.Model):
    subject = models.CharField(max_length=200)
    sender = models.CharField(max_length=200, default='Alex Recker')
    sender_address = models.CharField(max_length=200, default='alex@reckerfamily.com')
    post = models.OneToOneField(Post)
    sent = models.DateTimeField(default=datetime.datetime.now())

