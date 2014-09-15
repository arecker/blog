import unittest
import os
import shutil


from blog import Utility


class Helpers:
	pass


class UtilityTest(unittest.TestCase):


	def setUp(self):
		self.public = os.path.join(Utility.ROOT, 'test_public')
		if not os.path.exists(self.public):
			os.mkdir(self.public)


	def tearDown(self):
		shutil.rmtree(self.public)


	def check_file_for_dummy_title(self, path):
		with open(path) as file:
			contents = file.read()
		return '<title>Dummy</title>' in contents


	def test_utility_paths(self):
		self.assertEqual(os.path.basename(Utility.ROOT), 'Blog')
		self.assertEqual(os.path.basename(Utility.TEMPLATES), 'templates')
		self.assertEqual(os.path.basename(Utility.POSTS), 'posts')
		self.assertEqual(os.path.basename(Utility.DOCS), 'docs')


	def test_render_html_from_template(self):
		data = None
		html = Utility.render_html_from_template(template="dummy.html", data=data, test=True)
		self.assertTrue(html is not None)
		self.assertTrue('<title>Dummy</title>' in html)


	def test_write_page(self):
		data = None
		Utility.write_page(template="dummy.html", data=data, name="find_me.html", path=self.public, test=True)
		self.assertTrue(os.path.exists(os.path.join(self.public, 'find_me.html')))
		self.assertTrue(self.check_file_for_dummy_title(os.path.join(self.public, 'find_me.html')))



	def test_write_route(self):
		data = None
		Utility.write_route(template="dummy.html", data=data, route="im-a-route", root=self.public, test=True)
		self.assertTrue(os.path.exists(os.path.join(self.public, 'im-a-route')))
		self.assertTrue(self.check_file_for_dummy_title(os.path.join(self.public, 'im-a-route', 'index.html')))



if __name__ == '__main__':
	unittest.main()