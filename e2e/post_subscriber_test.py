"""
1. Subscriber signs up for blog with email
2. New blog post created
3. Email sent out
4. Subscriber clicks unsubscribe link in email
5. Subscriber unsubscribes
6. Another post created
7. Email sent out

Assert: subscriber does not get email
"""


from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils.text import slugify
from django.core import mail
from django.utils import timezone
import re
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from subscribing.models import Subscriber, PostNewsletter
from blogging.models import Post


class PostSubscriberTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.email = 'jonnystorm@gmail.com'
        self.full_text = False


    def _subscribe(self):
        data = {
            'email': self.email,
            'full_text': self.full_text
        }
        response = self.client.post('/api/subscribers/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscriber.objects.count(), 1)
        self.assertIsNotNone(Subscriber.objects.first().key)


    def _unsubscribe(self, key):
        count = Subscriber.objects.count()
        response = self.client.delete('/api/subscribers/{0}/'.format(key))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscriber.objects.count(), count - 1)


    def _create_post(self, title):
        count = Post.objects.count()
        p = Post()
        p.title = title
        p.slug = slugify(title)
        p.body = 'This is the **body** of a post entitled {0}'.format(title)
        p.save()
        self.assertEqual(Post.objects.count(), count + 1)
        return p


    def _create_newsletter(self, post):
        count = PostNewsletter.objects.count()
        n = PostNewsletter()
        n.post = post
        n.send_on_save = True
        n.timestamp = timezone.now()
        n.save()
        self.assertEqual(PostNewsletter.objects.count(), count + 1)


    def _get_key_from_email(self):
        self.assertEqual(len(mail.outbox), 1)
        line = [ l for l in mail.outbox[0].body.splitlines() if 'Unsubscribe here' in l ][0]
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
        self.assertEqual(len(urls), 1)
        url = urlparse(urls[0]).path
        key = url.rsplit('/', 2)[1]
        return key


    def test_it(self):
        self._subscribe()
        post = self._create_post('Test Post 1')
        self._create_newsletter(post)
        key = self._get_key_from_email()
        self._unsubscribe(key)
        mail.outbox = []
        post = self._create_post('Test Post 2')
        self._create_newsletter(post)
        self.assertEqual(len(mail.outbox), 0)