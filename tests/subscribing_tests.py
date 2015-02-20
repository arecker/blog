from django.test import TestCase
from rest_framework.test import APITestCase
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


    def test_unicode_representation(self):
        sub = models.Subscriber()
        sub.email = 'canyouseeme@maybe.com'
        self.assertEquals(str(sub), sub.email)


class TestSubscriberAPI(APITestCase):
    def setUp(self):
        self.subscribe_endpoint = '/api/subscribing/subscribe/'
        self.unsubscribe_endpoint = '/api/subscribing/unsubscribe/'

    def test_subscriber_add(self):
        data = {'email': 'test_subscriber_add@yahoo.com', 'full_text': 'false'}
        response = self.client.post(self.subscribe_endpoint, data, format='json')
        self.assertEqual(response.status_code, 201)

        matching = models.Subscriber.objects.filter(email='test_subscriber_add@yahoo.com')
        self.assertEquals(len(matching), 1)


    def test_subscriber_add_duplicate(self):
        data = {'email': 'twice@yahoo.com', 'full_text': 'false'}
        response = self.client.post(self.subscribe_endpoint, data, format='json')
        self.assertEqual(response.status_code, 201)

        matching = models.Subscriber.objects.filter(email='twice@yahoo.com')
        self.assertEquals(len(matching), 1)

        # Save it again
        response = self.client.post(self.subscribe_endpoint, data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_unsubscribe(self):
        data = {'email': 'dontLikeEmails@yahoo.com', 'full_text': 'false'}
        response = self.client.post(self.subscribe_endpoint, data, format='json')
        self.assertEqual(response.status_code, 201)

        # Get Key
        unsub = models.Subscriber.objects.get(email='dontLikeEmails@yahoo.com').unsubscribe_key
        self.assertTrue(unsub != '' and unsub is not None)

        # Unsubscribe
        response = self.client.get(self.unsubscribe_endpoint + '?unsubscribe=' + unsub, format='json')
        self.assertTrue(response.status_code, 201)

        # Check DB
        matching = models.Subscriber.objects.filter(email='dontLikeEmails@yahoo.com').count()
        self.assertEquals(matching, 0)


    def test_subscribe_bad_data(self):
        data = {} # send empty data
        response = self.client.post(self.subscribe_endpoint, data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_subscribe_bad_method(self):
        data = {}
        response = self.client.get(self.subscribe_endpoint, data, format='json')
        self.assertEquals(response.status_code, 404)


    def test_unsubscribe_bad_method(self):
        response = self.client.post(self.unsubscribe_endpoint , format='json')
        self.assertTrue(response.status_code, 404)


    def test_unsubscribe_no_key(self):
        response = self.client.get(self.unsubscribe_endpoint, format='json')
        self.assertEquals(response.status_code, 400)