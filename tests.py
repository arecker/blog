from django.test import SimpleTestCase
from os.path import join as Join, abspath, splitext
filepath, extension = splitext(__file__)
from slugify import slugify as Slugify
from os import listdir
from everything import HomePage, ArchivesPage
DOCS = abspath(Join(filepath, '..', 'docs'))
POSTS = abspath(Join(filepath, '..', 'posts'))


class HomePageTests(SimpleTestCase):
    def setUp(self):
        self.TestHomePage = HomePage(Join(DOCS, 'test_home.md'))


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
        expected = listdir(POSTS)
        self.assertEqual(actual, expected, "Archives page model returned wrong number of posts")