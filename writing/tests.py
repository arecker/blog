from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from .models import Post, Author

import os


class WritingSanityTests(TestCase):
    fixtures = [
        os.path.join(
            settings.BASE_DIR,
            'writing/fixtures/users.json'
        ),
        os.path.join(
            settings.BASE_DIR,
            'writing/fixtures/writing.json'
        )
    ]

    def test_sanity(self):
        self.assertEqual(2, User.objects.count())
        self.assertEqual(2, Author.objects.count())
        self.assertEqual(46, Post.objects.count())
