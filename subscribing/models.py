from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.template.loader import get_template
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from blog.utils import get_uuid_pk, to_full_url, shorten_url

from uuid import uuid4
import logging


logger = logging.getLogger(__name__)


class SubscriberQuerySet(models.QuerySet):
    def verified(self):
        return self.filter(is_verified=True)

    def active(self):
        return self.filter(is_active=True)

    def receiving_mail(self):
        return self.active().verified()


class Subscriber(models.Model):
    objects = SubscriberQuerySet.as_manager()

    id = get_uuid_pk()

    verify_key = models.UUIDField(default=uuid4,
                                  editable=False)
    unsubscribe_key = models.UUIDField(default=uuid4,
                                       editable=False)

    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    subscribed = models.DateTimeField(auto_now_add=True)
    verified = models.DateTimeField(editable=False, null=True)
    unsubscribed = models.DateTimeField(editable=False, null=True)

    def __unicode__(self):
        return self.email

    @property
    def unsubscribe_link(self):
        rel = reverse('unsubscribe', args=[str(self.unsubscribe_key)])
        full = to_full_url(relative_url=rel)
        return shorten_url(long_url=full)

    @property
    def verify_link(self):
        rel = reverse('verify', args=[str(self.verify_key)])
        full = to_full_url(relative_url=rel)
        return shorten_url(long_url=full)

    def send_verify_email(self):
        if self.is_verified:
            error = 'tried to send verification email to {}, ' \
                    'who is already verified'
            logger.warn(error.format(self.email))
            return

        body = get_template('verify.txt').render({'recipient': self})
        try:
            send_mail('Could you verify your email?',
                      body,
                      'alex@reckerfamily.com',
                      [self.email])
            logger.info('sent verification email to {}'.format(self.email))
        except Exception as e:
            logger.error('error sending verification email to {}'.format(self.email))
            logger.critical(e)

    def verify(self):
        if self.is_verified:
            logger.warning('tried to verify {}, who is already verified'
                           .format(self.email))
            return

        if not self.is_active:
            logger.warning('tried to verify {}, who is inactive'
                           .format(self.email))

        self.is_verified = True
        self.verified = timezone.now()

        try:
            return self.save()
        except Exception as e:
            logger.error('could not verify {}'.format(self.email))
            logger.critical(e)

    def unsubscribe(self):
        if not self.is_active:
            logger.warning('tried to unsubscribe {}, who is inactive'
                           .format(self.email))

        self.is_active = False
        self.unsubscribed = timezone.now()

        try:
            return self.save()
        except Exception as e:
            logger.error('could not unsubscribe {}'.format(self.email))
            logger.critical(e)


class Email(models.Model):
    id = get_uuid_pk()

    subject = models.CharField(max_length=78)
    sender = models.EmailField(default='alex@reckerfamily.com')
    body = models.TextField()

    is_sent = models.BooleanField(default=False, editable=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    sent = models.DateTimeField(null=True, editable=False)

    def __unicode__(self):
        return self.subject

    def send(self):
        recipients = Subscriber.objects.receiving_mail()

        if self.is_sent:
            return

        for r in recipients:
            template = get_template('email.txt')
            rendered_body = template.render({'recipient': r,
                                             'body': self.body})
            try:
                send_mail(self.subject,
                          rendered_body,
                          self.sender,
                          [r.email])
                logger.info('sent "{}" to {}'
                            .format(self.subject, r.email))
            except Exception as e:
                logger.error('error sending "{}" to {}'
                             .format(self.subject, r.email))
                logger.critical(e)

        self.is_sent = True
        self.sent = timezone.now()
        self.save()

        logger.info('sent {} to {} subscriber(s)'
                    .format(self.subject, len(recipients)))
