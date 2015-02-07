from django.test import TestCase
import datetime
from Blog.apps.Blogging import models

class TestPost(TestCase):


    def test_slug(self):
        myPost = models.Post()
        myPost.title = 'This is my First Post'
        myPost.date = datetime.datetime.now()
        myPost.save()
        self.assertEquals(myPost.slug, 'this-is-my-first-post')


    def test_get_truncated_description(self):
        myPost = models.Post()
        myPost.title = 'Another Post'
        myPost.date = datetime.datetime.now()
        myPost.description = 'This is a really long description.'
        myPost.save()

        actual = myPost.get_truncated_description(length=11)
        self.assertEquals(actual, 'This is a...')
        self.assertEquals(len(actual), 12)


    def test_get_truncated_description_safe(self):
        """
        should return empty string if no description yet
        """
        self.assertEquals('', models.Post().get_truncated_description())


    def test_convert_alts_to_captions(self):
        def remove_white(str):
            return str.replace('\n', '').replace(' ', '')


        post = models.Post()
        post.title = 'Test Caption Converter'
        post.date = datetime.datetime.now()
        post.description = 'This is a post to test the Caption COnverter'
        post.body = """![This is the caption](http://media.alexrecker.com/images/portrait.jpg)"""

        expected = u"""<figure class="image">
            <img alt="This is the caption" src="http://media.alexrecker.com/images/portrait.jpg" />
            <figcaption>This is the caption</figcaption>
        </figure>
        """

        actual = post.render_html()

        self.assertTrue(remove_white(expected) in remove_white(actual))
