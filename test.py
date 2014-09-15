import unittest
import os
import shutil


from blog import Utility, Post


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


	def test_read_in_json_from_path(self):
		data = Utility.read_in_json_from_path(os.path.join(Utility.DOCS, 'test.json'))
		self.assertEqual(data["poo"], "bah")


class PostTest(unittest.TestCase):

	def setUp(self):
		post_path = os.path.join(Utility.DOCS, '1900-01-10.md')
		self.post = Post(post_path) 


	def tearDown(self):
		pass


	def test_post_init(self):
		self.assertEqual(self.post.title, 'The Great Test Post')
		self.assertEqual(self.post.description, 'This is a test post, man.')
		self.assertEqual(self.post.image, 'flyingMonkeys.jpeg')
		self.assertTrue('This is the first line.' in self.post.body)


if __name__ == '__main__':
	unittest.main()