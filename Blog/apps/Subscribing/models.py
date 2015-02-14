from django.db import models
from django.template.loader import render_to_string
from django.core.mail import get_connection, EmailMultiAlternatives
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
    send_on_save = models.BooleanField(verbose_name='Send on Save', default=False)


    @staticmethod
    def send_emails(newsletter, subscribers):
        import logging
        logger = logging.getLogger(__name__)
        try:
            logger.debug('EMAIL: Opening connection for newsletter {news_id}'.format(news_id=newsletter.pk))
            connection = get_connection()
            connection.open()
            for sub in subscribers:
                html_content = render_to_string('subscribing/email.html', {'post': newsletter.post, 'sub': sub })
                text_content = newsletter.post.body
                msg = EmailMultiAlternatives(newsletter.subject, text_content, newsletter.sender_address, [sub.email], connection=connection)
                msg.attach_alternative(html_content, "text/html")
                try:
                    logger.debug('EMAIL: sending newsletter {news_id} to subscriber {sub_id}'.format(news_id=newsletter.pk, sub_id=sub.pk))
                    msg.send()
                except:
                    logger.error('EMAIL: error sending newsletter {news_id} to subscriber {sub_id}'.format(news_id=newsletter.pk, sub_id=sub.pk))
                    raise
            logger.debug('EMAIL: closing connection for {news_id}'.format(news_id=newsletter.pk))
            connection.close()
        except:
            logger.error('EMAIL: error sending newsletter {news_id}'.format(news_id=newsletter.pk))
            raise


    def save(self, *args, **kwargs):
        if self.send_on_save:
            subs = Subscriber.objects.all()
            Newsletter.send_emails(self, subs)
            self.send_on_save = False
        return super(Newsletter, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.subject

