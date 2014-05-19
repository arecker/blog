import unittest
from models import ConfigurationModel, Post, CacheWriter
from os import listdir
from os.path import join


class TestPosts(unittest.TestCase):
    def setUp(self):
        self.config = ConfigurationModel()
        self.test_post = Post(join(self.config.posts, '2014-04-03.md'))


    def test_parse_post_file(self):
        self.assertEqual(self.test_post.title, 'Welcome Home')
        self.assertEqual(self.test_post.date, '2014-04-03')
        self.assertEqual(self.test_post.description, 'Wordpress has served me well, but my soul longs for the wilderness.  Retreat with me into the backwoods of the Internet.')
        self.assertEqual(self.test_post.image, None)
        self.assertEqual(self.test_post.pubDate, 'Thu, 03 Apr 2014 05:00:00 -0000')


class TestCacheWriter(unittest.TestCase):
    def setUp(self):
        self.cw = CacheWriter()
        self.config = ConfigurationModel()

    def test_cw_init(self):
        post_files = list(reversed(sorted(listdir(self.config.posts))))
        self.assertEqual(self.cw.PostFiles, post_files)
        self.cw.Write()


def run():
    test_classes_to_run = [TestPosts, TestCacheWriter]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)