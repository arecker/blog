import click
import jinja2
import os
import json
import markdown
import slugify
import datetime


class Data:
	pass


class Utility:
	"""
	File IO, getting paths, and general crap work
	"""

	# Paths
	ROOT = os.path.dirname(os.path.realpath(__file__))
	TEMPLATES = os.path.join(ROOT, 'templates')
	POSTS = os.path.join(ROOT, 'posts')
	PUBLIC = os.path.join(ROOT, 'public')
	DOCS = os.path.join(ROOT, 'docs')
	if not os.path.exists(PUBLIC):
		os.mkdir(PUBLIC)


	@staticmethod
	def render_html_from_template(template, data, test=False):
		"""
		takes a template name and data
		returns an html string
		"""
		env = jinja2.Environment(loader=jinja2.FileSystemLoader(Utility.TEMPLATES))
		if test:
			env = jinja2.Environment(loader=jinja2.FileSystemLoader(Utility.DOCS))
		j_template = env.get_template(template)
		return j_template.render(data = data)


	@staticmethod
	def write_page(template, data, name, path=PUBLIC, test=False):
		"""
		takes a template name, page data, and a page name
		writes the page name to the path
		"""
		output = Utility.render_html_from_template(template=template, data=data, test=test)
		with open(os.path.join(path, name), 'wb') as file:
			file.write(output)


	@staticmethod
	def write_route(template, data, route, root=PUBLIC, test=False):
		"""
		creates a folder in public
		and writes data into an index.html within that folder
		"""
		path = os.path.join(root, route)
		os.makedirs(path)
		Utility.write_page(template=template, data=data, name="index.html", path=path, test=test)


	@staticmethod
	def read_in_json_from_path(path):
		with open(path, 'r') as file:
			data = json.load(file)
		return data


class Homepage:
	"""
	this class reads in the homepage file
	and creates a data packet
	"""
	def __init__(self, path=os.path.join(Utility.ROOT, 'homepage.json')):
		data = Utility.read_in_json_from_path(path)
		self.projects = data.projects
		self.friends = data.friends
		self.posts = None
		self.latest = None


class Post:
	"""
	this class holds the posts object,
	as well as some other helpful post related methods
	"""
	def __init__(self, path):
		data = self.parse_post_from_md(path)
		self.title = data.title
		self.date = data.date
		self.body = data.body
		self.link = data.link
		self.description = data.description
		self.image = data.image		


	@classmethod
	def parse_post_from_md(cls, path):
		"""
		reads in file, parses to html, and returns
		good stuff
		"""

		file = open(path, 'r')
		contents = file.read()
		file.close()

		md = markdown.Markdown(extensions = ['extra', 'meta'])
		html = md.convert(contents)
		meta = md.Meta

		data = Data()
		data.body = html
		data.title = meta["title"][0]
		data.link = slugify.slugify(data.title)
		data.description = meta["description"][0]
		try:
			data.image = meta["image"][0]
		except KeyError:
			data.image = None
		data.date = Post.parse_date_from_filename(path)

		return data


	@classmethod
	def parse_date_from_filename(cls, path):
		"""
		converts a post filename to a python datetime
		"""
		name, ext = os.path.splitext(os.path.basename(path))
		return datetime.datetime.strptime(name, "%Y-%m-%d").date()


	@classmethod
	def convert_alts_to_captions(cls, path):
		"""
		parses html and creates figure/caption groups from img/alt tags
		"""
		pass


class KeyManager:
	AUTHENTICATED = True
	try:
		data = Utility.read_in_json_from_path(os.path.join(Utility.ROOT, 'keys.json'))
		ADMIN = data["admin"]
		APP = data["app"]
		EMAIL = data["email"]
		EMAIL_PASSWORD = data["email_password"]
	except IOError:
		authenticated = False


@click.group()
def cli():
    """
    This is the script for my blog.
    It does things.
    """
    pass


if __name__ == '__main__':
    cli()