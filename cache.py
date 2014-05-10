import json
import sys
from os.path import splitext, join, dirname
from os import listdir
from slugify import slugify
from BeautifulSoup import BeautifulSoup
from markdown2 import markdown_path
from jinja2 import Environment, FileSystemLoader
from unidecode import unidecode as decode
import datetime
import time
from email import utils


class ConfigurationModel:
    def __init__(self):
        self.root = splitext(__file__)[0]
        self.pages = join(dirname(self.root), 'content', 'pages.json')
        self.posts = join(dirname(self.root), 'content', 'posts')
        self.templates = join(dirname(self.root), 'templates')
        self.cache = join(dirname(self.root), 'cache')
        self.static = join(dirname(self.root), 'static')
        self.url = 'alexrecker.com'


class Headline:
    def __init__(self, title, image, caption, link):
        self.title = title
        self.image = image
        self.caption = caption
        self.link = link


class Project:
    def __init__(self, title, subtitle, caption, image, link):
        self.title = title
        self.subtitle = subtitle
        self.caption = caption
        self.image = image
        self.link = link


class Friend:
    def __init__(self, title, subtitle, image, link):
        self.title = title
        self.subtitle = subtitle
        self.image = image
        self.link = link


class Post:
    def __init__(self, title, date, description, body, image=None):
        self.title = decode(title)
        self.link = decode(slugify(title))
        self.date = date
        self.description = decode(description)
        self.image = image
        self.body = decode(body)
        self.pubDate = utils.formatdate(time.mktime(datetime.datetime.strptime(date, '%Y-%m-%d').timetuple()))
        self.rssBody = self.body.replace('<', '&lt;').replace('>', '&gt;')


class SitemapItem:
    def __init__(self, loc, changefreq = 'weekly'):
        self.loc = 'http://' + loc
        self.changefreq = changefreq


class CacheWriter:
    def __init__(self):
        # Get Config Object
        self.config = ConfigurationModel()

        # Read in json for page content
        data = json.load(open(self.config.pages))
        self.Headlines = data["Headlines"]
        self.Projects = data["Projects"]
        self.Friends = data["Friends"]

        # Read in list of posts
        self.PostFiles = reversed(sorted(listdir(self.config.posts)))
        self.Posts = []


    def WriteHomePage(self):
        headlines = []
        for headline in self.Headlines:
            headlines.append(
                Headline(
                    title = headline["title"],
                    image = headline["image"],
                    caption = headline["caption"],
                    link = headline["link"]
                )
            )

        self.WriteOutToTemplate(template_name='home.html', collection=headlines)


    def WriteProjectsPage(self):
        projects = []
        for project in self.Projects:
            projects.append(
                Project(
                    title = project["title"],
                    subtitle = project["subtitle"],
                    caption = project["caption"],
                    image = project["image"],
                    link = project["link"]
                )
            )

        self.WriteOutToTemplate(template_name='projects.html', collection=projects)


    def WriteFriendsPage(self):
        friends = []
        for friend in self.Friends:
            friends.append(
                Friend(
                    title = friend["title"],
                    subtitle = friend["subtitle"],
                    image = friend["image"],
                    link = friend["link"]
                )
            )

        self.WriteOutToTemplate(template_name='friends.html', collection=friends)


    def WritePosts(self):
        self.Posts = []
        for post in self.PostFiles:
            self.Posts.append(
                self.CreatePost(post)
            )

        # Write to archives
        self.WriteOutToTemplate(template_name='archives.html', collection=self.Posts)

        # Write out to individual posts
        for post in self.Posts:
            self.WriteOutToTemplate(template_name='post.html', collection=post, post_name = str(post.link) + '.html')


    def CreatePost(self, post):
        """Creates Post from raw MD"""
        markdown = markdown_path(join(self.config.posts, post))
        raw = BeautifulSoup(markdown)
        metas = []
        for thing in raw.p:
            if thing != '\n':
                metas.append(thing)

        title = metas[0]
        description = metas[1]
        try:
            image = metas[2].string.replace('<!--', '') #TODO: Not sure how this works
        except IndexError:
            image = None # no banner image - that's fine
        body = markdown
        date = post.split('.')[0]

        return Post(
            title = title,
            date = date,
            description = description,
            image = image,
            body = body,
        )


    def UpdateSitemap(self):
        collection = []

        # Homepage
        collection.append(SitemapItem(
            loc = self.config.url + '/'
        ))

        # Pages
        for page in ['archives', 'projects', 'friends']: # TODO: Maybe jsonfiy these
            collection.append(SitemapItem(
                loc = self.config.url + '/' + page + '/'
            ))

        # Posts
        for post in self.Posts:
            collection.append(SitemapItem(
                loc = self.config.url + '/' + post.link + '/'
            ))

        self.WriteOutToTemplate('sitemap.xml', collection)


    def UpdateFeed(self):
        self.WriteOutToTemplate('feed.xml', collection = self.Posts)


    def WriteOutToTemplate(self, template_name, collection, post_name=None):
        ENV = Environment(loader=FileSystemLoader(self.config.templates))
        template = ENV.get_template(template_name)

        if post_name is not None:
            template_name = post_name # Writing out to individual post file

        print('+ Caching ' + template_name)
        with open(join(self.config.cache, template_name), 'wb') as file:
            file.write(template.render(
                collection = collection
            ))



### Commandline Interface
import click
@click.command()
@click.option('--posts', 'depth', flag_value='posts', default=True, help="Updates posts files, archives, sitemap, and RSS feed")
@click.option('--full', 'depth', flag_value='full', help="Updates everything")
def HitIt(depth):
    """
        This is the master caching script for the blog.  It reads in everything from the content directory,
        then pipes it through Jinja templates into the caching directory.
    """
    print('Updating Posts:')
    cw = CacheWriter()
    cw.WritePosts()
    cw.UpdateSitemap()
    cw.UpdateFeed()

    if depth == 'full':
        print('\nUpdating Pages:')
        cw.WriteHomePage()
        cw.WriteProjectsPage()
        cw.WriteFriendsPage()

if __name__ == '__main__':
    HitIt()
