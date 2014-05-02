### Imports
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown_path as MD
from BeautifulSoup import BeautifulSoup as HTML, Comment
from slugify import slugify as Slug
from os.path import join, abspath, splitext
from os import listdir
import operator


### Global Variables
filepath, extension = splitext(__file__)
PAGES = abspath(join(filepath, '..', 'content/pages'))
POSTS = abspath(join(filepath, '..', 'content/posts'))
CACHE = abspath(join(filepath, '..', 'cache'))
TEMPLATES = abspath(join(filepath, '..', 'templates'))
ENV = Environment(loader=FileSystemLoader('templates'))

# Dictionary of Posts / Slugs
POST_LIST = listdir(POSTS)
dictionary = []
for file in POST_LIST:
    comments = HTML(MD(join(POSTS, file))).findAll(text = lambda text: isinstance(text, Comment))
    key = Slug(comments[0])
    dictionary.append((key, file))
DICTIONARY = dict(dictionary)

### Page Models
class HomePage:
    def __init__(self, PATH=join(PAGES, 'home.md')):
        raw = MD(PATH)
        self.headlines = []
        for p in HTML(raw).findAll('p'):
            title = p.string
            for _thumbnail, _description, _link in ((p.findNext('ul').findChildren()),):
                self.headlines.append(Headline(Title=title, Thumbnail=_thumbnail.string, Description=_description.string, Link=_link.string))


class ArchivesPage:
    def __init__(self):
        file_list = reversed(sorted(POST_LIST))
        self.archives = []
        self.files = []
        for file in file_list:
            self.files.append(file)
            raw = MD(join(POSTS, file))
            date, ext = file.split('.')
            comments = HTML(raw).findAll(text = lambda text: isinstance(text, Comment))
            for _title, _description in (comments,):
                self.archives.append(Archive(Title=_title.string.replace('<!--', ''), Date=date, Description=_description.string.replace('<!--', '')))
        self.archives = reversed(sorted(self.archives, key=operator.attrgetter('date')))

				
class ProjectsPage:
    def __init__(self, PATH=join(PAGES, 'projects.md')):
        raw = MD(PATH)
        self.projects = []
        for p in HTML(raw).findAll('p'):
            title, subtitle = p.string.split(': ')
            for _thumbnail, _description, _link in ((p.findNext('ul').findChildren()),):
                self.projects.append(Project(Title=title, Subtitle=subtitle, Thumbnail=_thumbnail.string, Description=_description.string, Link=_link.string))


class FriendsPage:
    def __init__(self, PATH=join(PAGES, 'friends.md')):
        raw = MD(PATH)
        self.friends = []
        for p in HTML(raw).findAll('p'):
            title, description = p.string.split(': ')
            for link, thumbnail in ((p.findNext('ul').findChildren()),):
                self.friends.append(Friend(Title=title, Description=description, Thumbnail=thumbnail.string, Link=link.string))


class Post:
    def __init__(self, slug, ROOT=POSTS):
        ## Get Post from slug
        the_one = DICTIONARY[slug]
        self.date, extension = the_one.split('.')
        raw = MD(join(ROOT, the_one))
        comments = HTML(raw).findAll(text = lambda text: isinstance(text, Comment))
        self.title = comments[0].string.replace('<!--', '')
        self.description = comments[1].string.replace('<!--', '')
        self.link = slug

        # Get Banner
        banner_tag = HTML(raw).find(attrs={"alt": "banner"})
        _banner = banner_tag['src']
        raw = raw.replace('<p>' + str(banner_tag) + '</p>', '')

        # Replace images with thumbnails
        for element in HTML(raw).findAll('img'):
            try:
                _caption = element['alt']
                _src = element['src']
                thumbnail = Thumbnail(SRC=_src, Caption=_caption)
                raw = raw.replace('<p>' + str(element) + '</p>', str(thumbnail.element))
            except KeyError:
                pass #Trying to parse the banner.  Stahp it.

        self.body = Body(Banner=_banner, Text=raw)


### Helper Classes
class Thumbnail:
    def __init__(self, SRC, Caption):
        element = u'<div class="row">'
        element += u'<div class="col-md-4 col-md-offset-4">'
        element += u'<div class="thumbnail"><a href="' + SRC + '">'
        element += u'<img src="' + SRC + u'" /></a>'
        element += u'<div class="caption">'
        element += u'<p>' + Caption + u'</p>'
        element += u'</div></div></div></div>'
        self.element = element

		
class Headline:
    def __init__(self, Title, Thumbnail, Description, Link):
        self.title = Title
        self.thumbnail = Thumbnail
        self.description = Description
        self.link = Link


class Archive:
    def __init__(self, Title, Date, Description):
        self.title = Title
        self.date = Date
        self.description = Description
        self.link = Slug(Title)
		

class Body:
    def __init__(self, Banner, Text):
        self.banner = Banner
        self.text = Text

		
class Friend:
    def __init__(self, Title, Description, Link, Thumbnail):
        self.title = Title
        self.description = Description
        self.link = Link
        self.thumbnail = Thumbnail
		
		
class Project:
    def __init__(self, Title, Subtitle, Description, Thumbnail, Link):
        self.title = Title
        self.subtitle = Subtitle
        self.description = Description
        self.thumbnail = Thumbnail
        self.link = Link
		

### Helper Methods
def RefreshHome():
    template = ENV.get_template('home.html')
    with open(join(CACHE, 'pages', 'home.html'), 'wb') as file:
        file.write(template.render(HomePage = HomePage()))


def RefreshArchives():
    template = ENV.get_template('archives.html')
    with open(join(CACHE, 'pages', 'archives.html'), 'wb') as file:
        file.write(template.render(ArchivesPage = ArchivesPage()).encode('ascii', 'ignore'))


def RefreshProjects():
    template = ENV.get_template('projects.html')
    with open(join(CACHE, 'pages', 'projects.html'), 'wb') as file:
        file.write(template.render(ProjectsPage = ProjectsPage()))


def RefreshFriends():
    template = ENV.get_template('friends.html')
    with open(join(CACHE, 'pages', 'friends.html'), 'wb') as file:
        file.write(template.render(FriendsPage = FriendsPage()))


def RefreshPosts():
    template = ENV.get_template('post.html')
    REV_DICT_LIST = {v:k for k, v in DICTIONARY.items()} # Reverse Dictionary
    for file in POST_LIST:
        with open(join(CACHE, 'posts', REV_DICT_LIST[file] + '.html'), 'wb') as out:
            out.write(template.render(Post = Post(REV_DICT_LIST[file])).encode('ascii', 'ignore'))
            print('    Post: ' + REV_DICT_LIST[file])


### Action
print('Caching Home Page')
RefreshHome()
print('Caching Archives Page')
RefreshArchives()
print('Caching Projects Page')
RefreshProjects()
print('Caching Frineds Page')
RefreshFriends()
print('Caching Posts')
RefreshPosts()
print('Done!')
