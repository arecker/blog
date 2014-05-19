from markdown2 import markdown_path
from BeautifulSoup import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from os import listdir
from os.path import splitext, join, dirname
from ntpath import basename
from slugify import slugify
from unidecode import unidecode
import datetime, time
from email import utils
import json


class ConfigurationModel:
    def __init__(self):
        self.root = splitext(__file__)[0]
        self.pages = join(dirname(self.root), 'content', 'pages.json')
        self.posts = join(dirname(self.root), 'content', 'posts')
        self.templates = join(dirname(self.root), 'templates')
        self.cache = join(dirname(self.root), 'cache')
        self.static = join(dirname(self.root), 'static')
        self.env = Environment(loader=FileSystemLoader(self.config.templates))


class Post:
    def __init__(self, file):
        html = markdown_path(file)
        soup = BeautifulSoup(html)
        metas = []
        for thing in soup.p:
            if thing != '\n':
                metas.append(thing)

        self.title = metas[0]
        self.link = slugify(self.title)
        self.description = unidecode(metas[1])
        self.date = basename(file).split('.')[0]
        try:
            self.image = metas[2]
        except IndexError:
            self.image = None
        self.body = html
        self.pubDate = utils.formatdate(time.mktime(datetime.datetime.strptime(self.date, '%Y-%m-%d').timetuple())) # Never touching this again.
        self.rssBody = self.body.replace('<', '&lt;').replace('>', '&gt;')


class Thumbnail:
    def __init__(self, title, image, link, subtitle = None, caption = None):
        self.title = title
        self.image = image
        self.subtitle = subtitle
        self.caption = caption
        self.link = link


class CacheWriter:
    def __init__(self):
        self.config = ConfigurationModel()

        # Read in json for page content
        data = json.load(open(self.config.pages))
        self.Headlines = data["Headlines"]
        self.Projects = data["Projects"]
        self.Friends = data["Friends"]

        # Read in list of posts
        self.PostFiles = list(reversed(sorted(listdir(self.config.posts))))
        self.Posts= []

        for file in self.PostFiles:
            self.Posts.append(Post(join(self.config.posts, file)))


    def Write(self):
        template = self.config.env.get_template('post.html')

        # Individual Posts
        for post in self.Posts:
            with open(join(self.config.cache, post.link + '.html'), 'wb') as file:
                file.write(template.render(
                    collection = post
                ))

        # RSS
        template = self.config.env.get_template('feed.xml')
        with open(join(self.config.cache, 'feed.xml'), 'wb') as file:
            file.write(template.render(
                collection = self.Posts
            ))

