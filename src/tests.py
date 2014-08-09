from models import Post, ContentItems
import unittest


class TestPost(unittest.TestCase):
    def setUp(self):
        self.post = Post('test/1900-01-01.md')


    def test_post_creation(self):
        self.assertEqual(self.post.title, 'My Test Post')
        self.assertEqual(self.post.description, 'This is a description of my test post.')
        self.assertEqual(self.post.date, '1900-01-01')
        self.assertTrue('This is the first paragraph' in self.post.body)


    def test_to_rss_body(self):
        self.post.to_rss()
        self.assertTrue('This is the first paragraph' in self.post.rss_body)


    def test_to_rss_date(self):
        self.post.to_rss()
        self.assertTrue('Mon, 01 Jan 1900' in self.post.rss_date)


class TestContentItems(unittest.TestCase):
    def setUp(self):
        self.ci = ContentItems('test/pages.json')


    def test_projects(self):
        self.assertEqual(self.ci.projects[0].title, 'MJ Art Inspiration')
        self.assertEqual(self.ci.projects[1].subtitle, 'A Chrome Extension')
        self.assertEqual(self.ci.projects[2].image, 'bobross.jpg')


    def test_friends(self):
        self.assertEqual(self.ci.friends[0].title, 'A Glorious Mystery')
        self.assertEqual(self.ci.friends[1].subtitle, 'Blog by Ben Parks')
        self.assertEqual(self.ci.friends[2].link, 'http://brewerdigital.com')


if __name__ == '__main__':
	unittest.main()