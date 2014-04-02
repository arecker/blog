from django.shortcuts import render_to_response
from django.conf.urls import patterns
from os.path import join as Join
from os.path import splitext, abspath
from os import listdir
from markdown2 import markdown_path
from BeautifulSoup import BeautifulSoup

### Global Variables
filepath, extension = splitext(__file__)
PAGES = abspath(Join(filepath, '..', 'pages'))
POSTS = abspath(Join(filepath, '..', 'posts'))


### Models
class Post:
    def __init__(self, meta_title, meta_description, meta_canonical, title, body):
        self.Meta_title = meta_title
        self.Meta_description = meta_description
        self.Meta_canonical=meta_canonical
        self.Title = title
        self.Body = body


### Controllers
def GetHome(request):
    post = ParseMarkdown(Join(PAGES, 'home.md'))
    return render_to_response('base.html', {
        'post': post,
    })

def GetArchives(request):
    m_title = "Archives"
    m_description = "Placeholder"
    m_canonical = "Placeholder"
    title = "Archives"
    body = "Archives page here."
    post = Post(m_title, m_description, m_canonical, title, body)
    return render_to_response('base.html', {
        'post': post,
    })

def GetProjects(request):
    post = ParseMarkdown(Join(PAGES, 'projects.md'))
    return render_to_response('base.html', {
        'post': post,
    })

def GetFriends(request):
    post = ParseMarkdown(Join(PAGES, 'friends.md'))
    return render_to_response('base.html', {
        'post': post,
    })

def GetPost(request, slug):
    lookup = []
    for post in listdir(POSTS):
        (date, key) = post.replace('.md', '').split('_')
        lookup.append((key, date))

    try:
        lookup = dict(lookup)
        file = lookup[slug] + '_' + slug + '.md'
        PATH = Join(POSTS, file)
    except:
        PATH = Join(PAGES, '404.md')

    post = ParseMarkdown(PATH)
    return render_to_response('base.html', {
        'post': post,
    })

### Helpers
def ParseMarkdown(PATH):
    # Splits MD into metadata and body,
    # Then signs a new post with the appropriate properties
    for _metadata, _body in (markdown_path(PATH).split('[go]'),): # '[go]' is the magic separator
        for _meta_title, _meta_description, _meta_canonical, _title in (BeautifulSoup(_metadata).findAll('li'),):
            meta_title = _meta_title.string
            meta_description = _meta_description.string
            meta_canonical = _meta_canonical.string
            title = _title.string
        body = _body
    return Post(meta_title=meta_title, meta_description=meta_description, meta_canonical=meta_canonical, title=title, body=body)



### Routes
urlpatterns = patterns('',
    (r'^$', GetHome),
    (r'^archives/', GetArchives),
    (r'^projects/', GetProjects),
    (r'^friends/', GetFriends),
    (r'^(?P<slug>[^/]+)', GetPost),
)
