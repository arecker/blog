import unittest
import datetime
from Blog.apps.Blogging import models

class TestPost(unittest.TestCase):


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


if __name__ == '__main__':
    unittest.main()
