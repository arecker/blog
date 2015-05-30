from django.db import models
from blogging.models import Post
from .email import PostEmail
import uuid
import logging
logger = logging.getLogger(__name__)


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    full_text = models.BooleanField(default=False)
    key = models.UUIDField(primary_key=True, default=uuid.uuid4)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return self.email


class PostNewsletter(models.Model):
    post = models.ForeignKey(Post)
    timestamp = models.DateTimeField(auto_created=True)
    send_on_save = models.BooleanField(default=False, verbose_name='Send on Save')


    def __unicode__(self):
        return self.post.title


    def save(self):
        if self.send_on_save:
            for sub in Subscriber.objects.all():
                PostEmail(sub, self.post).send()
                self.send_on_save = False
                logging.info('PostNewsletter {0} sent to {1}'.format(self.post.title, sub.email))
        super(PostNewsletter, self).save()
