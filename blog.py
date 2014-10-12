import click
import jinja2
import os
import json
import markdown
import slugify
import datetime
import codecs
import shutil
import bs4
import flask
import requests
import tabulate
import smtplib
import PyRSS2Gen


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
	def write_route(template, data, route, root=PUBLIC, test=False, file_override="index.html"):
		"""
		creates a folder in public
		and writes data into an index.html within that folder
		"""
		path = os.path.join(root, route)
		os.makedirs(path)
		Utility.write_page(template=template, data=data, name=file_override, path=path, test=test)


	@staticmethod
	def create_feed_route(root=PUBLIC):
		"""
		PyRSS2Gen has it's own built in rss writer.
		this method simply creates a folder for it's file
		"""
		path = os.path.join(root, 'feed')
		os.makedirs(path)


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


	@staticmethod
	def get_latest_post():
		"""
		returns only the latest post
		"""
		#latest_file = sorted(os.listdir(Utility.POSTS))[-1]
		#latest_post = Post(os.path.join(Utility.POSTS, latest_file))
		return Post.get_all_posts()[0]


class RSSItem:
	"""
	a feed item is constructed with a post
	converts post attributes to xml friendly
	stuff
	"""
	def __init__(self, post):
		self.post = post
		self.rss = PyRSS2Gen.RSS2(
			title = "Blog by Alex Recker",
			link = "http://alexrecker.com",
			description = "Hey - my name is Alex Recker.  I like to write words.",

			items = [
				PyRSS2Gen.RSSItem(
			         title = self.post.title,
			         link = "http://alexrecker.com/" + self.post.link,
			         description = self.post.body,
			         guid = PyRSS2Gen.Guid("http://alexrecker.com/" + self.post.link),
			         pubDate = datetime.datetime.combine(self.post.date, datetime.datetime.min.time())
			   	)
			]
		)

	def write(self):
		self.rss.write_xml(open(os.path.join(Utility.PUBLIC, 'feed', "index.xml"), "w"))


class Email:
	"""
	Definition class for an email.
	Constructs header and email body
	"""
	def __init__(self, data):
		self.sender = 'Alex Recker'
		self.recipient = data.email
		self.subject = data.post.title
		self.post = data.post
		self.unsubscribe_key = data.unsubscribe_key
		self.full_text = data.full_text

		self.headers = "\r\n".join(["from: " + self.sender,
		"subject: " + self.subject,
		"to: " + self.recipient,
		"mime-version: 1.0",
		"content-type: text/html"])


	def send(self, test=False):
		self.body = Utility.render_html_from_template(template="email.html", data=self)
		self.content = self.headers + "\r\n\r\n" + self.body
		self.content = self.content.encode('ascii', 'ignore')

		if test:
			Utility.write_page(template='email.html', data=self, name=self.recipient + '.html', path=os.curdir)
			exit()

		# logging in for each email is not ideal,
		# but i was having issues keeping the tunnel open
		session = smtplib.SMTP('smtp.gmail.com', 587)
		session.ehlo()
		session.starttls()
		session.login(KeyManager.EMAIL, KeyManager.EMAIL_PASSWORD)
		session.sendmail(KeyManager.EMAIL, self.recipient, self.content)
		session.close()


class KeyManager:
	AUTHENTICATED = True
	try:
		data = Utility.read_in_json_from_path(os.path.join(Utility.ROOT, 'keys.json'))
		ADMIN = data["admin"]
		APP = data["app"]
		EMAIL = data["email"]
		EMAIL_PASSWORD = data["email_password"]
	except IOError:
		AUTHENTICATED = False


class WebServer:
	def __init__(self):
		self.app = flask.Flask(__name__)
		self.app.debug = True
		self.app.add_url_rule('/', 'index', self.index)
		self.app.add_url_rule('/<slug>/', 'slug', self.get_slug)
		self.app.run()


	def index(self):
		return self.read_file('index.html')


	def get_slug(self, slug):
		try:
			return self.read_file(slug)
		except IOError:
			return self.read_file(os.path.join(slug, 'index.html'))


	def read_file(self, target):
		with open(os.path.join(Utility.PUBLIC, target)) as file:
			return file.read()


def refresh_public():
	posts = Post.get_all_posts()
	latest = posts[0]
	Utility.drop_public()

	# Static Resources
	Utility.rebuild_static()

	# Homepage
	homepage = Homepage(posts=posts)	
	Utility.write_page(template="home.html", data=homepage, name="index.html")

	# Posts
	for post in posts:
		Utility.write_route(template="post.html", data=post, route=post.link)

	# RSS
	Utility.create_feed_route()
	rss = RSSItem(latest)
	rss.write()


def get_subscriber_list():
    if KeyManager.AUTHENTICATED:
        key = KeyManager.ADMIN
        url = "http://api.alexrecker.com/email/subscriber/list/?admin=" + key
        resp = requests.get(url=url)
        data = json.loads(resp.text)
        return data
    else:
        click.echo("this app is not authenticated")
        exit()


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
	refresh_public()


@cli.command(name="serve")
@click.option('-r', is_flag=True, help="refresh cache")
def cli_serve(r=False):
	"""
	runs local web server
	"""
	if r:
		refresh_public()
	server = WebServer()


@cli.group(name="email")
def cli_email():
	"""
	manages email subscribers
	"""
	pass


@cli_email.command(name="list")
def cli_email_list():
	"""
	lists subscribers
	"""
	data = get_subscriber_list()
	count = len(data)
	if count is 0:
		print('There are no subscribers.')
		exit()
	elif count is 1:
		print('There is 1 subscriber\n')
	else:
		print('There are ' + str(count) + ' subscribers.\n')

	table = []
	for sub in data:
		table.append([sub["email"], sub["full_text"], sub["unsubscribe_key"]])
	print(tabulate.tabulate(table, headers=["Email", "Full Text", "Key"]))


@cli_email.command(name="delete")
@click.option('--key', prompt="Unsubscribe Key")
def email_delete(key):
	"""
	deletes a subscriber (key required)
	"""
	url = "http://api.alexrecker.com/email/subscriber/delete?unsubscribe=" + key
	resp = requests.get(url=url)
	click.echo('Subscriber removed') #TODO: handle server side error


@cli_email.command(name="send")
@click.option('--test', is_flag=True, help="writes out email to local html files")
def email_send(test=False):
	"""
	sends latest post to subscribers
	"""
	if not KeyManager.AUTHENTICATED:
		click.echo('this app is not authenticated')
		exit()
	latest = Post.get_latest_post()
	emails = []

	for sub in get_subscriber_list():
		data = Data()
		data.email = sub["email"]
		data.unsubscribe_key = sub["unsubscribe_key"]
		data.full_text = sub["full_text"]
		data.post = latest
		emails.append(Email(data))

	print('You are about to send out ' + str(len(emails)) + ' emails.')
	print('Post: ' + latest.title)
	if not click.confirm('Church?'):
		print('Whatever')
		exit()

	with click.progressbar(emails, label="Sending...") as bar:
		for email in bar:
			email.send()	



if __name__ == '__main__':
	cli()