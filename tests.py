import unittest
from blog import *
from os import listdir
from os.path import join
from shutil import rmtree
from xml.etree import ElementTree


class TestPosts(unittest.TestCase):
    def setUp(self):
        self.config = ConfigurationModel()
        self.test_post = Post(join(self.config.posts, '2014-04-03.md'))


    def test_parse_post_file(self):
        self.assertEqual(self.test_post.title, 'Welcome Home')
        self.assertEqual(self.test_post.date, '2014-04-03')
        self.assertEqual(self.test_post.description, 'Wordpress has served me well, but my soul longs for the wilderness.  Retreat with me into the backwoods of the Internet.')
        self.assertEqual(self.test_post.image, None)
#        self.assertEqual(self.test_post.pubDate, 'Thu, 03 Apr 2014 05:00:00 -0000')
        self.assertTrue('Thu, 03 Apr 2014' in self.test_post.pubDate)


class TestCacheWriter(unittest.TestCase):
    def setUp(self):
        self.cw = CacheWriter(test = True)
        self.config = ConfigurationModel(test = True)
        self.cw.write(silent = True)


    def test_cw_init(self):
        post_files = list(reversed(sorted(listdir(self.config.posts))))
        self.assertEqual(self.cw.PostFiles, post_files)


    def test_cache_count(self):
        count = 0
        for post in self.cw.Posts:
            count = count + 1
        for page in ["404.html", "sitemap.xml", "feed.xml", "home.html"]:
            count = count + 1
        actual = len(listdir(self.config.cache))
        self.assertEqual(actual, count)


    def test_cache_file_names(self):
        list = []
        for post in self.cw.Posts:
            list.append(post.link + '.html')
        list.append('home.html')
        for page in ["feed.xml", "sitemap.xml", "404.html"]:
            list.append(page)
        list = sorted(list)
        self.assertEqual(sorted(listdir(self.config.cache)), list)


    def tearDown(self):
        rmtree(self.config.cache)


class TestXML(unittest.TestCase):
    def setUp(self):
        self.cw = CacheWriter(test = True)
        self.config = ConfigurationModel(test = True)
        self.cw.write(silent = True)


    def test_validate_rss_feed(self):
        with open(join(self.config.cache, 'feed.xml'), 'r') as file:
            rss_feed = file.read()

        try:
            feed = ElementTree.fromstring(rss_feed)
            success = True
        except:
            success = False

        self.assertTrue(success)


    def test_validate_sitemap(self):
        with open(join(self.config.cache, 'sitemap.xml'), 'r') as file:
            sitemap = file.read()

        try:
            feed = ElementTree.fromstring(sitemap)
            success = True
        except:
            success = False

        self.assertTrue(success)


    def tearDown(self):
        rmtree(self.config.cache)


class TestURLRoutes(unittest.TestCase):
    def setUp(self):
        self.cw = CacheWriter()
        self.cw.write(silent = True)
        from blog import app as Application
        self.tester = Application.test_client()


    def test_pages_route(self):
        response = self.tester.get('/')
        self.assertTrue("<title>Blog by Alex Recker</title>" in response.data)
        response = self.tester.get('/feed/')
        self.assertTrue('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">' in response.data)
        response = self.tester.get('/sitemap/')
        self.assertTrue('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' in response.data)
        response = self.tester.get('/definitely-not-a-page/')
        self.assertTrue('<title>Page Not Found | Blog by Alex Recker</title>' in response.data)


    def test_posts_route(self):
        for post in self.cw.Posts:
            response = self.tester.get('/' + post.link + '/')
            self.assertTrue('<title>' + post.title + ' | Blog by Alex Recker</title>' in response.data)
            self.assertTrue('<meta name="description" content="' + post.description + '">')


def run():
    """
    This method kind of sucks, but it's because of a bug in CLICK.
    unittest.main() breaks the command argument for some reason
    """
    test_classes_to_run = [TestPosts, TestCacheWriter,TestXML, TestURLRoutes]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)


if __name__ == '__main__':
    unittest.main()
