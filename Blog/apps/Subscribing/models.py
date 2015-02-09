from django.db import models
from Blog.apps.Blogging.models import Post
from uuid import uuid1
import datetime


class Email:
    def __init__(self, newsletter, subscriber):
        self.newsletter = newsletter
        self.subscriber = subscriber

        self.sender = 'Alex Recker'
        self.recipient = newsletter.sender_address
        self.subject = newsletter.subject
        self.post = newsletter.post
        self.unsubscribe_key = subscriber.unsubscribe_key
        self.full_text = subscriber.full_text
        self.headers = "\r\n".join(["from: " + self.sender,
        "subject: " + newsletter.subject,
        "to: " + subscriber.email,
        "mime-version: 1.0",
        "content-type: text/html"])


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
    send = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.send:
            for subscriber in Subscriber.objects.all():
                email = Email(self, subscriber)
                log = NewsletterLog(newsletter=self, subscriber=subscriber)
            self.send = False
        return super(Newsletter, self).save(*args, **kwargs)



class NewsletterLog(models.Model):
    newsletter = models.ForeignKey(Newsletter)
    subscriber = models.ForeignKey(Subscriber)
    time_started = models.DateTimeField(null=True)
    time_ended = models.DateTimeField(null=True)
    successful = models.NullBooleanField(default=None)


    def start(self):
        self.time_started = datetime.datetime.now()


    def stop(self):
        self.time_ended = datetime.datetime.now()
        super(NewsletterLog, self).save()

