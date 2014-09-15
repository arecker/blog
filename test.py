import unittest
import os

from blog import Utility


class Helpers:
	pass


class UtilityTest(unittest.TestCase):


	def setUp(self):
		# create test public directory
		self.public = os.path.join(Utility.ROOT, 'test_public')
		os.makedirs(self.public)


	def tearDown(self):
		os.rmtree(self.public)


	def test_utility_paths(self):
		self.assertEqual(os.path.basename(Utility.ROOT), 'Blog')
		self.assertEqual(os.path.basename(Utility.TEMPLATES), 'templates')
		self.assertEqual(os.path.basename(Utility.POSTS), 'posts')
		self.assertEqual(os.path.basename(Utility.DOCS), 'docs')


	def test_render_html_from_template(self):
		data = None
		html = render_html_from_template(template="dummy.html", data=data)
		self.assertTrue(html is not None)



if __name__ == '__main__':
	unittest.main()