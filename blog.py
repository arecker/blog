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
import urllib2
from tabulate import tabulate
from flask import Flask, Response
import smtplib
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


@app.route("/<slug>/")
def get_post(slug):
    if slug == 'robots.txt':
        with open(join(appconfig.cache, 'robots.txt'), 'r') as file:
            return Response(file.read(), mimetype='text/plain')
    try: # Return html page
        with open(join(appconfig.cache, slug + '.html'), 'r') as file:
            return file.read()
    except IOError:
        try: # Return xml page
            with open(join(appconfig.cache, slug + '.xml'), 'r') as file:
                return Response(file.read(), mimetype='text/xml')
        except IOError: # Return txt page
            try:
                with open(join(appconfig.cache, slug + '.txt'), 'r') as file:
                    return file.read()
            except IOError: # Return 404
                with open(join(appconfig.cache, '404.html'), 'r') as file:
                    return file.read()
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
    def __init__(self, test = False, posts_only=False):
        self.config = ConfigurationModel(test)

        self.PostFiles = list(reversed(sorted(listdir(self.config.posts))))
        self.Posts = []
        for file in self.PostFiles:
            self.Posts.append(Post(join(self.config.posts, file)))


        if not posts_only:
            # Read in json for page content
            data = json.load(open(self.config.pages))
            self.HeadlineContent = data["Headlines"]
            self.Headlines = []
            self.ProjectContent = data["Projects"]
            self.Projects = []
            self.FriendContent = data["Friends"]
            self.Friends = []
            self.Sites = []

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
            self.Sites.append('/')


    def write(self, silent):
        cache_package = []

        # Individual Posts
        for post in self.Posts:
            cache_package.append({
                "template": "post.html",
                "data": post
            })

        # Homepage
        home_data = {
            "latest": self.Posts[0],
            "posts": self.Posts,
            "friends": self.Friends,
            "projects": self.Projects
        }
        cache_package.append({
            "template": "home.html",
            "data": home_data
        })

        # RSS
        cache_package.append({
            "template": "feed.xml",
            "data": self.Posts[0]
        })

        # 404
        cache_package.append({
            "template": "404.html",
            "data": None
        })

        # Robots
        cache_package.append({
            "template": "robots.txt",
            "data": None
        })

        # Sitemap
        cache_package.append({
            "template": "sitemap.xml",
            "data": self.Sites
        })

        if silent:
            for item in cache_package:
                self.output(item["template"], item["data"])
        else:  
            with click.progressbar(cache_package, label="Caching pages") as bar:
                for item in bar:
                    self.output(item["template"], item["data"])


    def output(self, template, data):
        j_template = self.config.env.get_template(template)
        if template == 'post.html':
            template = data.link + '.html'
        with open(join(self.config.cache, template), 'wb') as file:
            file.write(j_template.render(data = data))


    @classmethod
    def get_latest_post(cls):
        return cls(posts_only=True).Posts[0]

        
#endregion

#region CLI
@click.group()
def cli():
    """
    This is the script for my blog.  It does things.
    """
    pass


@cli.command()
@click.option('--silent', is_flag=True, help="supress output")
def update(silent):
    """
    refresh the content cache
    """
    if not silent:
        print('Assembling content...')
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

@cli.group()
def email():
    """
    manages the email subscription engine
    """
    pass


def get_subscriber_list():
    """
    Gets a list of email subscribers from API
    """
    try:
        with open(join(dirname(appconfig.root),'.keys.json')) as file:
            data = json.load(file)
            admin_key = data["admin"]
    except IOError:
        admin_key = click.prompt('Admin Key')
    try:
        returned = urllib2.urlopen("http://api.alexrecker.com/email/subscriber/list/?admin=" + admin_key)
    except:
        print("Cannot reach API")
    return json.load(returned)


@email.command(name="list")
def email_list():
    """
    list subscribers
    """
    data = get_subscriber_list()
    count = len(data)
    if count is 0:
        print('There are no subscribers.')
        exit()
    elif count is 1:
        print('There is 1 subscriber')
        print("")
    else:
        print('There are ' + str(count) + ' subscribers.')
        print("")

    # Print Table
    table = []
    for sub in data:
        table.append([sub["email"], sub["full_text"], sub["unsubscribe_key"]])
    print tabulate(table, headers=["Email", "Full Text", "Key"])


@email.command(name="send")
@click.option('--test', is_flag=True, help="writes out email to html files")
def email_send(test=False):
    """
    sends latest blog post to subscribers
    """
    try:
        with open(join(dirname(appconfig.root),'.keys.json')) as file:
            data = json.load(file)
            email = data["email"]
            email_password = data["email_password"]
    except IOError:
        email = click.prompt('Email')
        email_password = click.prompt('Password')

    # Get Data
    post = CacheWriter.get_latest_post()
    subscribers = get_subscriber_list()

    print('You are about to send out ' + str(len(subscribers)) + ' emails.')
    print('Post: ' + post.title)
    if not click.confirm('Church?'):
        print('Whatever')
        exit()

    # Open Email Session
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.login(email, email_password)
    
    # Write and Send
    j_template = appconfig.env.get_template('email.html')
    if test:
        label = "Sending (test)"
    else:
        label = "Sending"
    with click.progressbar(subscribers, label=label) as bar:
        for sub in bar:
            headers = "\r\n".join(["from: Alex Recker",
                       "subject: " + post.title,
                       "to: " + sub["email"],
                       "mime-version: 1.0",
                       "content-type: text/html"])
            full = sub["full_text"]
            unsubscribe = sub["unsubscribe_key"]
            body = j_template.render(post = post, full = full, unsubscribe = unsubscribe)
            content = headers + "\r\n\r\n" + body
            if not test:
                session.sendmail(email, sub["email"], content)
            else:
                test_dir = join(dirname(appconfig.root), 'test_emails')
                if not exists(test_dir):
                    makedirs(test_dir)
                with open(join(test_dir, sub["email"] + '.html'), 'w+') as file:
                    file.write(body)


@email.command(name="delete")
@click.option('--key', prompt="Unsubscribe Key")
def email_delete(key):
    """
    deletes a subscriber (key required)
    """
    try:
        urllib2.urlopen("http://api.alexrecker.com/email/subscriber/delete?unsubscribe=" + key)
        print('Subscriber removed')
    except:
        print("Cannot reach API")
    


if __name__ == '__main__':
    cli()
#endregion
