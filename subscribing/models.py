from django.db import models
from blogging.models import Post
from .email import PostEmail
import uuid
import logging


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
                try:
                    PostEmail(sub, self.post).send()
                    self.send_on_save = False
                    self._log(sub)
                except Exception as e:
                    self._error(sub, e)
        super(PostNewsletter, self).save()


    def _log(self, sub):
        logger = logging.getLogger()
        logger.info('PostNewsletter {0} sent to {1}'.format(self.post.title, sub.email))


    def _error(self, sub, e):
        logger = logging.getLogger()
        logger.info('Error sending {0} to {1}: {2}'.format(self.post.title, sub.email, e))
