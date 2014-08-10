from models import Post, ContentItems
import utility
import unittest
import os
import ntpath


class TestPost(unittest.TestCase):
    def setUp(self):
        file = os.path.join(utility.PathGetter.get_test_docs_directory(), '1900-01-01.md')
        self.post = Post(file)


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
        file = os.path.join(utility.PathGetter.get_test_docs_directory(), 'pages.json')
        self.ci = ContentItems(file)


    def test_projects(self):
        self.assertEqual(self.ci.projects[0].title, 'MJ Art Inspiration')
        self.assertEqual(self.ci.projects[1].subtitle, 'A Chrome Extension')
        self.assertEqual(self.ci.projects[2].image, 'bobross.jpg')


    def test_friends(self):
        self.assertEqual(self.ci.friends[0].title, 'A Glorious Mystery')
        self.assertEqual(self.ci.friends[1].subtitle, 'Blog by Ben Parks')
        self.assertEqual(self.ci.friends[2].link, 'http://brewerdigital.com')


class TestPathGetter(unittest.TestCase):
    def setUp(self):
        pass


    def test_get_project_src(self):
        actual = utility.PathGetter.get_project_src()
        self.assertTrue(os.path.exists(actual))
        self.assertTrue('src' in actual)
        self.assertEqual(ntpath.basename(actual), 'src')


    def test_get_posts_directory(self):
        actual = utility.PathGetter.get_posts_directory()
        self.assertTrue(os.path.exists(actual))
        self.assertTrue('posts' in actual)
        self.assertEqual(ntpath.basename(actual), 'posts')


    def test_get_public_directory(self):
        actual = utility.PathGetter.get_public_directory()
        self.assertTrue(os.path.exists(actual))
        self.assertTrue('public' in actual)
        self.assertEqual(ntpath.basename(actual), 'public')


    def test_get_content_path(self):
        actual = utility.PathGetter.get_content_path()
        self.assertTrue(os.path.exists(actual))
        self.assertTrue('src/pages.json' in actual)
        self.assertEqual(ntpath.basename(actual), 'pages.json')


    def test_get_templates_directory(self):
        actual = utility.PathGetter.get_templates_directory()
        self.assertTrue(os.path.exists(actual))
        self.assertTrue('src/templates' in actual)
        self.assertEqual(ntpath.basename(actual), 'templates')


    def test_get_test_docs_directory(self):
        actual = utility.PathGetter.get_test_docs_directory()
        self.assertTrue(os.path.exists(actual))
        self.assertTrue('src/test_docs' in actual)
        self.assertEqual(ntpath.basename(actual), 'test_docs')


class TestKeyManager():
    def setUp(self):
        self.key_path = os.path.join(utility.PathGetter.get_test_docs_directory(), 'test_keys.json')


    def test_get_admin_key(self):
        actual = utility.KeyManager.get_admin_key(self.key_path)
        self.assertEqual(actual, "babababababababab")


    def test_get_app_key(self):
        actual = utility.KeyManager.get_app_key(self.key_path)
        self.assertEqual(actual, "lkajsdlfajsdlfja1234134")


    def test_get_email(self):
        actual = utility.KeyManager.get_email(self.key_path)
        self.assertEqual(actual, "bob@test.com")


    def test_get_email_password(self):
        actual = utility.KeyManager.get_email_password(self.key_path)
        self.assertEqual(actual, "bobMissesTheHood")

if __name__ == '__main__':
	unittest.main()