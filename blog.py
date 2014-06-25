#region Imports
from markdown2 import markdown_path
from BeautifulSoup import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from os import listdir, makedirs
from os.path import splitext, join, dirname, exists
from ntpath import basename
from slugify import slugify
from unidecode import unidecode
import datetime, time
from email import utils
import json
import click
import tests
from flask import Flask, Response
#endregion

#region Config Model
class ConfigurationModel:
    def __init__(self, test = False):
        self.root = splitext(__file__)[0]
        self.pages = join(dirname(self.root), 'content', 'pages.json')
        self.posts = join(dirname(self.root), 'content', 'posts')
        self.templates = join(dirname(self.root), 'templates')
        if test:
            test_dir = join(dirname(self.root), 'test_cache')
            if not exists(test_dir):
                makedirs(test_dir)
            self.cache = test_dir
        else:
            cache_dir = join(dirname(self.root), 'cache')
            if not exists(cache_dir):
                makedirs(cache_dir)
            self.cache = cache_dir
        self.static = join(dirname(self.root), 'static')
        self.env = Environment(loader=FileSystemLoader(join(dirname(self.root), 'templates')))
#endregion

#region Server
app = Flask(__name__)
appconfig = ConfigurationModel()
@app.route("/")
def get_home():
    home_page = open(join(appconfig.cache, 'home.html'), 'r').read()
    return home_page


@app.route("/sitemap.xml")
def get_site_map():
    xml = open(join(appconfig.cache, 'sitemap.xml'), 'r').read()
    return Response(xml, mimetype='text/xml')

@app.route("/feed/")
def get_feed():
    xml = open(join(appconfig.cache, 'feed.xml'), 'r').read()
    return Response(xml, mimetype='text/xml')


@app.route("/robots.txt")
def get_robotss():
    robots = open(join(appconfig.static, 'robots.txt'), 'r').read()
    return Response(robots, mimetype='text')


@app.route("/<slug>/")
def get_post(slug):
    try:
        post = open(join(appconfig.cache, slug + '.html'), 'r').read()
        return post
    except:
        missing_page = open(join(appconfig.cache, '404.html'), 'r').read()
        return missing_page
#endregion

#region Update
class Post:
    def __init__(self, file):
        html = markdown_path(file)
        soup = BeautifulSoup(html)
        metas = []
        for thing in soup.p:
            if thing != '\n':
                metas.append(thing)

        self.title =metas[0].replace('<!--', '')
        self.link = slugify(self.title)
        self.description = unidecode(metas[1])
        self.date = basename(file).split('.')[0]
        try:
            self.image = metas[2].replace('<!--', '')
        except IndexError:
            self.image = None
        self.body = unidecode(html)
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
    def __init__(self, test = False):
        self.config = ConfigurationModel(test)

        # Read in json for page content
        data = json.load(open(self.config.pages))
        self.HeadlineContent = data["Headlines"]
        self.Headlines = []
        self.ProjectContent = data["Projects"]
        self.Projects = []
        self.FriendContent = data["Friends"]
        self.Friends = []
        self.PostFiles = list(reversed(sorted(listdir(self.config.posts))))
        self.Posts = []
        self.Sites = []

        for file in self.PostFiles:
            self.Posts.append(Post(join(self.config.posts, file)))

        for headline in self.HeadlineContent:
            self.Headlines.append(Thumbnail(
                title = headline["title"],
                image = headline["image"],
                caption = headline["caption"],
                link = headline["link"]
            ))

        for project in self.ProjectContent:
            self.Projects.append(Thumbnail(
                title = project["title"],
                subtitle = project["subtitle"],
                image = project["image"],
                caption = project["caption"],
                link = project["link"]
            ))


        for friend in self.FriendContent:
            self.Friends.append(Thumbnail(
                title = friend["title"],
                subtitle = friend["subtitle"],
                image = friend["image"],
                link = friend["link"]
            ))

        for post in self.Posts:
            self.Sites.append('/' + post.link + '/')
        for page in ['', '/archives/', '/friends/', '/projects/']:
            self.Sites.append(page)


    def write(self, silent):
        pages = []

        # Individual Posts
        for post in self.Posts:
            pages.append({
                "template": "post.html",
                "data": post
            })

        # Archives
        pages.append({
            "template": "archives.html",
            "data": self.Posts
        })

        # RSS
        pages.append({
            "template": "feed.xml",
            "data": self.Posts
        })

        # Home
        pages.append({
            "template": "home.html",
            "data": self.Headlines
        })

        # Projects
        pages.append({
            "template": "projects.html",
            "data": self.Projects
        })

        # Friends
        pages.append({
            "template": "friends.html",
            "data": self.Friends
        })

        # Sitemap
        pages.append({
            "template": "sitemap.xml",
            "data": self.Sites
        })

        # 404
        pages.append({
            "template": "404.html",
            "data": None
        })

        if silent:
            work = pages
        else:
            work = click.progressbar(pages, label="Caching pages")
        for item in work:
            self.output(item["template"], item["data"])


    def output(self, template, data):
        j_template = self.config.env.get_template(template)
        if template == 'post.html':
            template = data.link + '.html'
        with open(join(self.config.cache, template), 'wb') as file:
            file.write(j_template.render(data = data))
#endregion

#region CLI
@click.group()
def cli():
    """
    This is the admin script for my blog.
    """
    pass


@cli.command()
@click.option('--silent', is_flag=True, help="supress output")
def update(silent):
    """
    refresh the content cache
    """
    cw = CacheWriter()
    cw.write(silent)


@cli.command()
@click.option('--debug', is_flag=True, help="local debugging web server")
def server(debug):
    """
    run the web server
    """
    if debug:
        app.debug = True
    app.run()


@cli.command()
def test():
    """
    run unit tests
    """
    tests.run()


@cli.command()
def email():
    """
    manages the email subscription engine
    """
    pass


cli.add_command(update)
cli.add_command(test)
cli.add_command(email)
if __name__ == '__main__':
    cli()
#endregion
