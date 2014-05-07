import json
from os.path import splitext, join, dirname
from os import listdir
from slugify import slugify
from BeautifulSoup import BeautifulSoup
from markdown2 import markdown_path
from jinja2 import Environment, FileSystemLoader
from unidecode import unidecode as decode


class ConfigurationModel:
    def __init__(self):
        filepath = splitext(__file__)[0]
        self.pages = join(dirname(filepath), 'content', 'pages.json')
        self.posts = join(dirname(filepath), 'content', 'posts')
        self.templates = join(dirname(filepath), 'templates')
        self.cache = join(dirname(filepath), 'cache')
        self.static = join(dirname(filepath), 'static')


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
        self.body = body


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
        self.Posts = reversed(sorted(listdir(self.config.posts)))


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
        posts = []
        for post in self.Posts:
            posts.append(
                self.CreatePost(post)
            )

        # Write to archives
        self.WriteOutToTemplate(template_name='archives.html', collection=posts)

        # Write out to individual posts
        for post in posts:
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
            image = metas[2].string.replace('<!--', '')
        except IndexError:
            image = None # no banner image - that's fine
        body = decode(markdown)
        date = post.split('.')[0]

        return Post(
            title = title,
            date = date,
            description = description,
            image = image,
            body = body
        )


    def WriteOutToTemplate(self, template_name, collection, post_name=None):
        ENV = Environment(loader=FileSystemLoader(self.config.templates))
        template = ENV.get_template(template_name)

        if post_name is not None:
            template_name = post_name # Writing out to individual post file

        with open(join(self.config.cache, template_name), 'wb') as file:
            file.write(template.render(
                collection = collection
            ))


if __name__ == '__main__':
    cw = CacheWriter()
    cw.WriteHomePage()
    cw.WriteProjectsPage()
    cw.WriteFriendsPage()
    cw.WritePosts()

