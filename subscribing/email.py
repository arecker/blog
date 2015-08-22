from django.core.mail import send_mass_mail
from django.conf import settings
from django.template.loader import get_template
from django.template import Context

import logging


logger = logging.getLogger()


class BaseEmail(object):
    def __init__(self, subject, recipients, content,
                 sender=settings.EMAIL_FROM):
        self.sender = sender
        self.subject = subject
        self.recipients = recipients
        self.content = content

    def send(self):
        try:
            message = (
                self.subject,
                self.content,
                self.sender,
                self.recipients,
            )
            send_mass_mail((message, ))
            logger.info('Emailed "{0}" to {1} recipients'.format(
                self.subject, len(self.recipients)
            ))

        except Exception as e:
            logger.error('Error sending "{0}": {1}'.format(
                self.subject, e.message
            ))


class VerifySubscriberEmail(BaseEmail):
    def __init__(self, subscriber):
        content = get_template('subscribing/verify.txt').render({
            'subscriber': subscriber,
            'SITE_DOMAIN': settings.SITE_DOMAIN
        })
        super(VerifySubscriberEmail, self).__init__(
            subject='Could you verify your email?',
            recipients=[subscriber.email, ],
            content=content
        )

    def send(self):
        super(VerifySubscriberEmail, self).send()
