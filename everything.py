from django.shortcuts import render_to_response
from django.conf.urls import patterns
from slugify import slugify as Slug
from os.path import join as Join
from os.path import splitext, abspath
from os import listdir
from markdown2 import markdown_path as MD
from BeautifulSoup import BeautifulSoup as HTML, Comment

### Global Variables
filepath, extension = splitext(__file__)
PAGES = abspath(Join(filepath, '..', 'pages'))
POSTS = abspath(Join(filepath, '..', 'posts'))
DOCS = abspath(Join(filepath, '..', 'docs'))


### Models
class Headline:
    def __init__(self, Title, Thumbnail, Description, Link):
        self.title = Title
        self.thumbnail = Thumbnail
        self.description = Description
        self.link = Link

class HomePage:
    def __init__(self, PATH=Join(PAGES, 'home.md')):
        raw = MD(PATH)
        self.headlines = []
        for p in HTML(raw).findAll('p'):
            title = p.string
            for _thumbnail, _description, _link in ((p.findNext('ul').findChildren()),):
                self.headlines.append(Headline(Title=title, Thumbnail=_thumbnail.string, Description=_description.string, Link=_link.string))


class Archive:
    def __init__(self, Title, Date, Description):
        self.title = Title
        self.date = Date
        self.description = Description
        self.link = Slug(Title)


class ArchivesPage:
    def __init__(self):
        file_list = reversed(sorted(listdir(POSTS)))
        self.archives = []
        self.files = []
        for file in file_list:
            self.files.append(file)
            raw = MD(Join(POSTS, file))
            date, ext = file.split('.')
            comments = HTML(raw).findAll(text = lambda text: isinstance(text, Comment))
            for _title, _description in (comments,):
                self.archives.append(Archive(Title=_title.string, Date=date, Description=_description.string))
        self.archives = sorted(self.archives)


class Thumbnail:
    def __init__(self, SRC, Caption):
        element = u'<div class="row">'
        element += u'<div class="col-md-4 col-md-offset-4">'
        element += u'<div class="thumbnail">'
        element += u'<img src="' + SRC + u'" />'
        element += u'<div class="caption">'
        element += u'<p>' + Caption + u'</p>'
        element += u'</div></div></div></div>'
        self.element = element


class Body:
    def __init__(self, Banner, Text):
        self.banner = Banner
        self.text = Text


class Post:
    def __init__(self, slug, ROOT=POSTS):

        ## Get Post from slug
        files = listdir(ROOT)
        dictionary = []
        for file in files:
            comments = HTML(MD(Join(ROOT, file))).findAll(text = lambda text: isinstance(text, Comment))
            key = Slug(comments[0])
            dictionary.append((key, file))
        dictionary = dict(dictionary)
        the_one = dictionary[slug]
        raw = MD(Join(ROOT, the_one))
        comments = HTML(raw).findAll(text = lambda text: isinstance(text, Comment))
        self.title = comments[0].string
        self.link = slug

        # Get Banner
        banner_tag = HTML(raw).find(attrs={"alt": "banner"})
        _banner = banner_tag['src']
        raw = raw.replace('<p>' + str(banner_tag) + '</p>', '')

        # Replace images with thumbnails
        for element in HTML(raw).findAll('img'):
            _caption = element['alt']
            _src = element['src']
            thumbnail = Thumbnail(SRC=_src, Caption=_caption)
            raw = raw.replace('<p>' + str(element) + '</p>', str(thumbnail.element))

        self.body = Body(Banner=_banner, Text=raw)



### Controllers
def GetHome():
    pass


def GetArchives():
    pass


def GetProjects():
    pass


def GetFriends():
    pass

def GetPost():
    pass

### Routes
urlpatterns = patterns('',
    (r'^$', GetHome),
    (r'^archives/', GetArchives),
    (r'^projects/', GetProjects),
    (r'^friends/', GetFriends),
    (r'^(?P<slug>[^/]+)', GetPost),
)
