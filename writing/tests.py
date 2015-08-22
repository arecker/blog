from django.test import TestCase
from django.conf import settings

from .models import Post

import os


class WritingSanityTests(TestCase):
    fixtures = [
        os.path.join(
            settings.BASE_DIR,
            'writing/fixtures/writing.json'
        )
    ]

    def test_sanity(self):
        self.assertEqual(46, Post.objects.count())
