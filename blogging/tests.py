from django.test import TestCase
from django.conf import settings
from .models import Post
import datetime
import os


class PostTests(TestCase):
    fixtures = [
        os.path.join(settings.BASE_DIR, 'blogging', 'fixtures', 'posts.json')
    ]


    def test_natural_order(self):
        """
        Posts should naturally come back in order of newest to oldest
        """
        posts = Post.objects.all()
        self.assertTrue(len(posts) > 1)
        cursor = datetime.date.today()
        for p in Post.objects.all():
            self.assertTrue(p.date <= cursor)
            cursor = p.date


    def test_convert_alts_to_captions(self):
        """
        Alt tags in markdown should be converted to figurecaptions
        """
        def remove_white(str):
            return str.replace('\n', '').replace(' ', '')


        post = Post()
        post.title = 'Test Caption Converter'
        post.slug = 'test-caption-converter'
        post.date = datetime.datetime.now()
        post.description = 'This is a post to test the Caption Converter'
        post.body = """![This is the caption](http://media.alexrecker.com/images/portrait.jpg)"""

        expected = u"""<figure class="image">
            <img alt="This is the caption" src="http://media.alexrecker.com/images/portrait.jpg" />
            <figcaption>This is the caption</figcaption>
        </figure>
        """

        actual = post.body_html
        self.assertTrue(remove_white(expected) in remove_white(actual))