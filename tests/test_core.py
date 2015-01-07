import unittest
from blog import core
import os


this_dir = os.path.dirname(os.path.realpath(__file__))


class TestConfig(unittest.TestCase):
    def test_read_config(self):
        config = core.Config()
        self.assertIsNotNone(config)



class TestPost(unittest.TestCase):
    def setUp(self):
        pass


    def test_get_all_posts(self):
        list = core.Post.get_all_posts()
        self.assertEquals(len(list), len(os.listdir(core.Config().posts)))