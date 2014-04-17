from django.shortcuts import render_to_response
from django.conf.urls import patterns
import operator
from slugify import slugify as Slug
from os.path import join as Join
from os.path import splitext, abspath
from os import listdir
from markdown2 import markdown_path as MD
from BeautifulSoup import BeautifulSoup as HTML, Comment
from django.views.decorators.cache import cache_page

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

    def __str__(self):
        return self.date


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
        self.archives = reversed(sorted(self.archives, key=operator.attrgetter('date')))


class Project:
    def __init__(self, Title, Subtitle, Description, Thumbnail, Link):
        self.title = Title
        self.subtitle = Subtitle
        self.description = Description
        self.thumbnail = Thumbnail
        self.link = Link


class ProjectsPage:
    def __init__(self, PATH=Join(PAGES, 'projects.md')):
        raw = MD(PATH)
        self.projects = []
        for p in HTML(raw).findAll('p'):
            title, subtitle = p.string.split(': ')
            for _thumbnail, _description, _link in ((p.findNext('ul').findChildren()),):
                self.projects.append(Project(Title=title, Subtitle=subtitle, Thumbnail=_thumbnail.string, Description=_description.string, Link=_link.string))


class Friend:
    def __init__(self, Title, Description, Link, Thumbnail):
        self.title = Title
        self.description = Description
        self.link = Link
        self.thumbnail = Thumbnail


class FriendsPage:
    def __init__(self, PATH=Join(PAGES, 'friends.md')):
        raw = MD(PATH)
        self.friends = []
        for p in HTML(raw).findAll('p'):
            title, description = p.string.split(': ')
            for link, thumbnail in ((p.findNext('ul').findChildren()),):
                self.friends.append(Friend(Title=title, Description=description, Thumbnail=thumbnail.string, Link=link.string))


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
        self.date, extension = the_one.split('.')
        raw = MD(Join(ROOT, the_one))
        comments = HTML(raw).findAll(text = lambda text: isinstance(text, Comment))
        self.title = comments[0].string
        self.description = comments[1].string
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



### Controllers
@cache_page(60 * 15)
def GetHome(request):
    return render_to_response('home.html', {
        'HomePage': HomePage(),
    })

@cache_page(60 * 15)
def GetArchives(request):
    return render_to_response('archives.html', {
        'ArchivesPage': ArchivesPage(),
    })

@cache_page(60 * 15)
def GetProjects(request):
    return render_to_response('projects.html', {
        'ProjectsPage': ProjectsPage(),
    })

@cache_page(60 * 15)
def GetFriends(request):
    return render_to_response('friends.html', {
        'FriendsPage': FriendsPage(),
    })

@cache_page(60 * 15)
def GetPost(request, slug):
    try:
        post = Post(slug)
    except KeyError:
        pass #404

    return render_to_response('post.html', {
        'post': post,
    })

### Routes
urlpatterns = patterns('',
    (r'^$', GetHome),
    (r'^archives/?$', GetArchives),
    (r'^projects/?$', GetProjects),
    (r'^friends/?$', GetFriends),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve'),
    (r'^(?P<slug>[^/]+)', GetPost),
)
