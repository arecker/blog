"""
This Script refreshes the cached pages.
"""

# Imports
import operator
from os import listdir
from os.path import splitext, join as Join, abspath
from markdown2 import markdown_path as MD
from BeautifulSoup import BeautifulSoup as HTML, Comment
from xml.sax import saxutils as su
from slugify import slugify as Slug

# PATHS
filepath, extension = splitext(__file__)
POSTS = abspath(Join(filepath, '..', 'Content/posts'))
PAGES = abspath(Join(filepath, '..', 'Content/pages'))
CACHE = abspath(Join(filepath, '..', 'Cache'))

# Models
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
        self.archives = reversed(sorted(self.archives, key=operator.attrgetter('date')))

################################################################################################################

##############################
########## ARCHIVES ##########
##############################

archives_page = ArchivesPage()
archive_soup = HTML(open(Join(CACHE, 'soups/archives.html')))
handle = '<div class="handle"></div>'

for item in archives_page.archives:
    element  = '<div class="col-md-6">'
    element += '<div class="media">'
    element += '<div class="media-body">'
    element += '<h3 class="media-heading">'
    element += '<a href="/' + item.link + '">'
    element += item.title
    element += '</a></h3>'
    element += '<p>' + item.description + '</p>'
    element += '<p><small>' + item.date + '</small></p></div></div></div>'
    element += handle
    archive_soup.find("div", {"class": "handle" }).replaceWith(element)

    # Handle all the unicode shit
    archive_soup = HTML(su.unescape(archive_soup.prettify()))

# Write Out to cache
file = open(Join(CACHE, 'pages/archives-cache.html'),"w")
file.write(archive_soup.prettify())
file.close()

################################################################################################################

##############################
########## HomePage ##########
##############################

home_page = HomePage()
homepage_soup = HTML(open(Join(CACHE, 'soups/homepage.html')))
handle = '<div class="handle"></div>'

for item in home_page.headlines:
    element  = '<div class="col-sm-6 col-md-4">'
    element += '<div class="thumbnail">'
    element += '<a href="/' + item.link + '"><img src="' + item.thumbnail + '" ></a>'
    element += '<div class="caption">'
    element += '<h3>' + item.title + '</h3>'
    element += '<p>' + item.description + '</p>'
    element += '</div></div></div>'
    element += handle
    homepage_soup.find("div", {"class": "handle" }).replaceWith(element)

    # Handle all the unicode shit
    homepage_soup = HTML(su.unescape(homepage_soup.prettify()))

# Write Out to cache
file = open(Join(CACHE, 'pages/homepage-cache.html'),"w")
file.write(homepage_soup.prettify())
file.close()

"""
 <div class="col-sm-6 col-md-4">
    <div class="thumbnail">
      <a href="/{{ headline.link }}"><img src="{{ headline.thumbnail }}" ></a>
      <div class="caption">
        <h3>{{ headline.title }}</h3>
        <p>{{ headline.description }}</p>
      </div>
    </div>
  </div>
"""