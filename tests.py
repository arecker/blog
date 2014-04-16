from django.test import SimpleTestCase
from os.path import join as Join, abspath, splitext
filepath, extension = splitext(__file__)
from slugify import slugify as Slugify
from BeautifulSoup import BeautifulSoup as HTML
from os import listdir
from everything import HomePage, ArchivesPage, Post, Thumbnail
DOCS = abspath(Join(filepath, '..', 'docs'))
POSTS = abspath(Join(filepath, '..', 'posts'))


class HomePageTests(SimpleTestCase):
    def setUp(self):
        self.TestHomePage = HomePage(Join(DOCS, 'home.md'))


    def test_count(self):
        """HomePage read in proper number of thumbnails"""
        actual = len(self.TestHomePage.headlines)
        expected = 2
        self.assertEqual(actual, expected, "Returned wrong count")


    def test_titles(self):
        """HomePage read in proper titles"""
        actual = self.TestHomePage.headlines[0].title
        expected = "Thumbnail 1"
        self.assertEqual(actual, expected, "Returned different titles")

        actual = self.TestHomePage.headlines[1].title
        expected = "Thumbnail 2"
        self.assertEqual(actual, expected, "Returned different titles")


    def test_descriptions(self):
        """HomePage read in proper descriptions"""
        actual = self.TestHomePage.headlines[0].description
        expected = "This is the first thumbnail"
        self.assertEqual(actual, expected, "Returned different descriptions")


    def test_links(self):
        """Homepage returned valid and proper slugs"""
        for headline in self.TestHomePage.headlines:
            self.assertEqual(headline.link, Slugify(headline.link), "Not a valid slug")

        actual = self.TestHomePage.headlines[0].link
        expected = 'link-1'
        self.assertEqual(actual, expected, "Returned incorrect link")

        actual = self.TestHomePage.headlines[1].link
        expected = 'some-dumb-link'
        self.assertEqual(actual, expected, "Returned incorrect link")


    def test_thumbs(self):
        """Homepage returned valid thumbnails"""
        actual = self.TestHomePage.headlines[0].thumbnail
        expected = 'thumbnail1.jpg'
        self.assertEqual(actual, expected, "Returned incorrect link")

        actual = self.TestHomePage.headlines[1].thumbnail
        expected = 'thumbnail2.jpg'
        self.assertEqual(actual, expected, "Returned incorrect link")


class ArchivePageTests(SimpleTestCase):
    def setUp(self):
        self.TestArchivesPage = ArchivesPage()


    def test_count(self):
        """Verifies number of posts"""
        actual = len(self.TestArchivesPage.archives)
        expected = len(listdir(POSTS))
        self.assertEqual(actual, expected, "Archives page model returned wrong number of posts")


    def test_order(self):
        actual = self.TestArchivesPage.files
        expected = list(reversed(sorted(listdir(POSTS))))
        self.assertEqual(actual, expected, "Posts came back in wrong order")


class PostTests(SimpleTestCase):
    def setUp(self):
        self.TestPost = Post(slug=u'test-post', ROOT=DOCS + '/test_posts')


    def test_title(self):
        """Verifies Test Post title"""
        actual = self.TestPost.title
        expected = "Test Post"
        self.assertEqual(actual, expected, "Returned wrong post title")


    def test_slug(self):
        """Verifies matching slug"""
        actual = self.TestPost.link
        expected = 'test-post'
        self.assertEqual(actual, expected, "Returned wrong slug")


    def test_banner(self):
        """Verifies banner embed was removed from body"""
        actual = str(self.TestPost.body.text)
        bad = '![banner](brucebanner.jpg)'
        self.assertFalse(bad in actual, "Banner embed was not removed from post")

    def test_thumbnail(self):
        """Verifies original thumbnail embed was removed from body"""
        actual = str(self.TestPost.body.text)
        bad = '![thumbnail](jumbalaya.jpg "This is my favorite jumbalaya.")'
        self.assertFalse(bad in actual, "Thumbnail was left in body as original embed")

        """Verifies Thumbnail was created properly"""
        actual = Thumbnail(SRC="jumbalaya.jpg", Caption="This is my favorite jumbalaya.").element
        expected = u'<div class="row"><div class="col-md-4 col-md-offset-4"><div class="thumbnail"><img src="jumbalaya.jpg" /><div class="caption"><p>This is my favorite jumbalaya.</p></div></div></div></div>'
        self.assertEqual(actual, expected, "That's not the thumbnail I was expecting")

    def test_post_body(self):
        """Verifes test markdown post produced the expected html body"""
        actual = str(self.TestPost.body.text).replace('\n', '')
        expected = open(Join(DOCS, 'test_post.html'), 'r').read().replace('\n', '')
        self.assertEqual(actual, expected, "That's not the body I was expecting")

