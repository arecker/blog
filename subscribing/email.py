from django.core.mail import send_mass_mail, send_mail
from django.conf import settings
from django.template.loader import get_template

from post_office import mail

import logging


logger = logging.getLogger()


class BaseEmail(object):
    def __init__(self, subject, recipients, content,
                 sender=settings.EMAIL_FROM):
        self.sender = sender
        self.subject = subject
        self.recipients = recipients
        self.content = content

    def mass_send(self):
        messages = []
        for r in self.recipients:
            messages.append((
                self.subject,
                self.content,
                self.sender,
                [r],
            ))
        try:
            send_mass_mail(tuple(messages))
            logger.info('Emailed "{0}" to {1}'.format(
                self.subject, len(self.recipients)
            ))

        except Exception as e:
            logger.error('Error sending "{0}": {1}'.format(
                self.subject, e.message
            ))

    def send(self):
        self.recipients = ['alex@reckerfamily.com', ]
        try:
            mail.send(self.recipients,
                      self.sender,
                      self.subject,
                      self.content)
        except Exception as e:
            logger.error('Error sending "{0}" to {1}: {2}'.format(
                self.subject, self.recipients[0], e.message
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


class PostEmail(BaseEmail):
    def __init__(self, subscriber, post):
        content = get_template('subscribing/post.txt').render({
            'subscriber': subscriber,
            'post': post,
            'SITE_DOMAIN': settings.SITE_DOMAIN
        })
        super(PostEmail, self).__init__(
            subject='{0} | Blog by Alex Recker'.format(post.title),
            recipients=[subscriber.email, ],
            content=content
        )


class NewsletterEmail(BaseEmail):
    def __init__(self, newsletter, recipients):
        super(NewsletterEmail, self).__init__(
            subject=newsletter.subject,
            recipients=[r.email for r in recipients],
            content=newsletter.content
        )

    def send(self):
        super(NewsletterEmail, self).mass_send()
