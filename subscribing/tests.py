from django.test import TestCase
from django.core import mail
from .models import Subscriber
from .email import PostEmail
from blogging.models import Post


class EmailTests(TestCase):
    def setUp(self):
        self.sub = sub = Subscriber()
        sub.email = 'jack@test.com'
        sub.full_text = False
        sub.save()

        self.post = post = Post()
        post.title = 'Some Test'
        post.slug = 'some-test'
        post.description = 'This is a test post.'
        post.body = 'What?  Just a test body.'
        post.save()


    def test_send(self):
        e = PostEmail(self.sub, self.post)
        e.send()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Some Test')
        self.assertEqual(mail.outbox[0].to[0], 'jack@test.com')