from django.test import TestCase
from django.core import mail
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Subscriber
from .email import PostEmail
from blogging.models import Post
import os


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


class SubscribersAPITests(APITestCase):
    fixtures = [
        os.path.join(settings.BASE_DIR, 'subscribing', 'fixtures', 'subscribers.json')
    ]


    def setUp(self):
        self.client = APIClient()


    def test_create(self):
        data = {
            'email': 'newSubscriber@test.com',
            'full_text': False
        }
        response = self.client.post('/api/subscribers/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sub = Subscriber.objects.get(email='newSubscriber@test.com')
        self.assertEqual(sub.email, data['email'])
        self.assertEqual(sub.full_text, data['full_text'])
        self.assertIsNotNone(sub.key)


    def test_destroy(self):
        sub = Subscriber.objects.first()
        response = self.client.delete('/api/subscribers/{0}/'.format(sub.key))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscriber.objects.filter(email=sub.email).count(), 0)


    def test_list_forbidden(self):
        response = self.client.get('/api/subscribers/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_detail_forbidden(self):
        key = Subscriber.objects.first().key
        response = self.client.get('/api/subscribers/{0}/'.format(key))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_authenticated_list(self):
        User.objects.create_superuser('newadmin', '', 'adminpassword')
        self.client.login(username='newadmin', password='adminpassword')
        response = self.client.get('/api/subscribers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_authenticated_detail(self):
        User.objects.create_superuser('newadmin', '', 'adminpassword')
        key = Subscriber.objects.first().key
        self.client.login(username='newadmin', password='adminpassword')
        response = self.client.get('/api/subscribers/{0}/'.format(key))
        self.assertEqual(response.status_code, status.HTTP_200_OK)