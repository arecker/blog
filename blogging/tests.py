from django.test import TestCase
from .models import Post
import datetime


class PostTests(TestCase):
    def test_convert_alts_to_captions(self):
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