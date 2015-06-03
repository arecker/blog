from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings


class PostEmail(object):
    def __init__(self, subscriber, post):
        subject = post.title
        from_email = settings.EMAIL_FROM
        to_email = subscriber.email

        data = Context({
            'subscriber': subscriber,
            'post': post,
            'SITE_DOMAIN': settings.SITE_DOMAIN # TODO: Crap
        })

        text_content = get_template('emails/post.txt').render(data)
        html_content = get_template('emails/post.html').render(data)
        self.msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        self.msg.attach_alternative(html_content, "text/html")


    def send(self):
        self.msg.send()
