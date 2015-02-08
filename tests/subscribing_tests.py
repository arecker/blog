from django.test import TestCase
import datetime
from Blog.apps.Subscribing import models


class TestSubscriber(TestCase):
    def test_generate_key(self):
        sub = models.Subscriber()
        sub.email = 'alex@reckerfamily.com'
        sub.save()
        self.assertTrue(sub.unsubscribe_key != '' and sub.unsubscribe_key is not None)


    def test_generate_key_persists(self):
        sub = models.Subscriber()
        sub.email = 'test@email.com'
        sub.save()
        key = sub.unsubscribe_key
        sub.save()
        self.assertEquals(key, sub.unsubscribe_key)


    def test_created_date(self):
        sub = models.Subscriber()
        sub.email = 'hello@test.com'
        sub.save()
        self.assertTrue(sub.subscribe_date is not None)
