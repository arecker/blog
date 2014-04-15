from django.shortcuts import render_to_response
from django.conf.urls import patterns
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
    def __init(self, Title, Date, Description):
        self.title = Title
        self.date = Date
        self.description = Description


class ArchivesPage:
    def __init__(self):
        file_list = listdir(POSTS)
        self.archives = []
        for file in file_list:
            raw = MD(Join(POSTS, file))
            date, ext = file.split('.')
            comments = HTML(raw).findAll(text = lambda text: isinstance(text, Comment))
            for _title, _description in (comments,):
                self.archives.append(Archive(Title=_title.string, Date=date.string, Description=_description.string))

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
