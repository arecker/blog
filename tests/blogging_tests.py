from django.test import TestCase
import datetime
from Blog.apps.Blogging import models, feed

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


class TestFeed(TestCase):
    def setUp(self):
        post1 = models.Post()
        post1.title = 'Test Post 1'
        post1.date = datetime.datetime.now()
        post1.description = 'this is test 1'
        post1.save()
        post2 = models.Post()
        post2.title = 'Test Post 2'
        post2.date = datetime.datetime.now()
        post2.description = 'this is test 2'
        post2.save()


    def test_valid_feed(self):
        # TODO: Validate RSS Somehow
        output = feed.RSSFeed().write()
        self.assertTrue(output is not None)
        self.assertTrue(output != '' and output != u'')


class TestPostManager(TestCase):
    def setUp(self):
        post1 = models.Post()
        post1.title = 'Test Post 1'
        post1.date = datetime.datetime.now() - datetime.timedelta(days=1)
        post1.description = 'this is test 1'
        post1.published = True
        post1.save()
        post2 = models.Post()
        post2.title = 'Test Post 2'
        post2.date = datetime.datetime.now()
        post2.description = 'this is test 2'
        post2.published = True
        post2.save()

    @staticmethod
    def unpublish_all():
        for post in models.Post.objects.all():
            post.published = False
            post.save()

    @staticmethod
    def publish_all():
        for post in models.Post.objects.all():
            post.published = True
            post.save()


    def test_latest(self):
        latest = models.Post.objects.latest()
        self.assertEquals(latest.title, 'Test Post 2')


    def test_latest_safe(self):
        # Should return none if no published posts
        TestPostManager.unpublish_all()

        try:
            latest = models.Post.objects.latest()
            self.assertEquals(latest, None)
        except:
            TestPostManager.publish_all()


    def test_all_feed_items(self):
        feed = models.Post.objects.all_feed_items()
        last_date = None
        for item in feed:
            if last_date:
                self.assertTrue(item['date'] < last_date)
            last_date = item['date']


    def test_all_feed_items_safe(self):
        TestPostManager.unpublish_all()
        try:
            feed = models.Post.objects.all_feed_items()
            self.assertTrue(feed is not None)
            self.assertTrue(feed != u'' or feed != '')
        except:
            TestPostManager.publish_all()


    def test_all_archives(self):
        archives = models.Post.objects.all_archives()
        for item in archives:
            self.assertTrue(item['title'] is not None)
            self.assertTrue(item['slug'] is not None)

        self.assertEquals(archives[0]['title'], 'Test Post 2')