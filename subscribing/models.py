from django.db import models
import logging

from uuid import uuid4

from .email import VerifySubscriberEmail, PostEmail


logger = logging.getLogger()


class SubscriberQuerySet(models.QuerySet):
    def verified(self):
        return self.filter(verified=True)


class Subscriber(models.Model):
    objects = SubscriberQuerySet.as_manager()
    key = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.verified:
            VerifySubscriberEmail(self).send()
        super(Subscriber, self).save(*args, **kwargs)

    def verify(self):
        if self.verified:
            return
        try:
            self.verified = True
            super(Subscriber, self).save()
            logger.info('{0} has been verified'.format(self.email))
        except Exception as e:
            logger.error('error verifying {0}: {1}'.format(
                self.email, e.message
            ))

    def send_post(self, post):
        PostEmail(self, post).send()

    def __unicode__(self):
        return self.email
