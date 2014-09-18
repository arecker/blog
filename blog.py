import click
import jinja2
import os
import json
import markdown
import slugify
import datetime
import codecs
import shutil
import BaseHTTPServer
import bs4


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
			output = bs4.BeautifulSoup(output).prettify()
			file.write(output.encode('utf-8'))


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
	def rebuild_static(root=PUBLIC):
		"""
		Drops and recopies the static libs into a public folder
		"""
		target = os.path.join(root, 'static')
		if os.path.exists(target):
			shutil.rmtree(target)
		shutil.copytree(os.path.join(Utility.ROOT, 'static'), target)


	@staticmethod
	def drop_public(root=PUBLIC):
		"""
		drops whole public directory
		"""
		for thing in os.listdir(root):
			try:
				shutil.rmtree(os.path.join(root, thing))
			except:
				os.remove(os.path.join(root, thing))



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
	def __init__(self, posts, path=os.path.join(Utility.ROOT, 'home.json')):
		data = Utility.read_in_json_from_path(path)
		self.projects = []
		for project in data["projects"]:
			data = Data()
			data.title = project["title"]
			data.caption = project["caption"]
			data.link = project["link"]
			data.image = project["image"]
			self.projects.append(data)

		#self.friends = data["friends"]
		self.posts = posts
		self.latest = posts[0]


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


	def __unicode__(self):
		return self.link


	def __str__(self):
		return self.link	


	@classmethod
	def parse_post_from_md(cls, path):
		"""
		reads in file, parses to html, and returns
		good stuff
		"""

		file = codecs.open(path, encoding="utf-8", mode="r")
		contents = file.read()
		file.close()

		md = markdown.Markdown(extensions = ['extra', 'meta'])
		html = md.convert(contents)
		meta = md.Meta

		data = Data()
		data.body = Post.convert_alts_to_captions(html)
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
	def convert_alts_to_captions(cls, html):
		"""
		parses html and creates figure/caption groups from img/alt tags
		![alt tag]('src')

		<img src="src" alt="">
		<figure class="image">
			<img alt="" src="">
			<figcaption>Caption here</figcaption>
		</figure>
		"""
		soup = bs4.BeautifulSoup(html)
		imgs = soup.find_all('img')
		for tag in imgs:
			src = tag['src']
			try:
				alt = tag['alt']
			except KeyError:
				alt = None
			tag.wrap(soup.new_tag('figure', { 'class': 'image'}))
			tag.parent['class'] = 'image'
			tag.insert_after(soup.new_tag('figcaption'))
			if alt:
				tag.next_sibling.string = alt
		return soup.prettify()


	@staticmethod
	def get_all_posts():
		"""
		returns a collection of post objects
		ordered by descending date
		"""
		posts = []
		files = os.listdir(Utility.POSTS)
		for file in files:
			posts.append(Post(os.path.join(Utility.POSTS, file)))
		posts.sort(key=lambda x: x.date, reverse=True)
		return posts



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


@cli.command(name="refresh")
def cli_refresh():
	"""
	refreshes html cache
	"""
	hopper = []

	posts = Post.get_all_posts()
	Utility.drop_public()

	# Static Resources
	Utility.rebuild_static()

	# Homepage
	homepage = Homepage(posts=posts)	
	Utility.write_page(template="home.html", data=homepage, name="index.html")

	# Posts
	for post in posts:
		Utility.write_route(template="post.html", data=post, route=post.link)


@cli.command(name="serve")
def cli_serve():
	"""
	runs local web server
	"""
	pass


if __name__ == '__main__':
    cli()