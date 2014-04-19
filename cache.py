"""
This Script refreshes the cached pages.
"""

# Imports
import operator
from os import listdir
from os.path import splitext, join as Join, abspath
from markdown2 import markdown_path as MD
from BeautifulSoup import BeautifulSoup as HTML, Comment
import slugify as Slug

# PATHS
filepath, extension = splitext(__file__)
POSTS = abspath(Join(filepath, '..', 'Content/posts'))
PAGES = abspath(Join(filepath, '..', 'Cache/pages'))
SOUPS = abspath(Join(filepath, '..', 'Cache/Soups'))

# Models
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


### ARCHIVES
archives_page = ArchivesPage()
archive_soup = HTML(open(Join(SOUPS, 'archives.html')))
#append_div = archive_soup.findAll("div", { "class" : "row" })

for item in ArchivesPage.archives:
    

"""
ARVCHIVE FORMAT
{% for archive in ArchivesPage.archives %}
			<div class="col-md-6">
				<div class="media">
		  			<div class="media-body">
		    			<h3 class="media-heading"><a href="/{{ archive.link }}">{{ archive.title }}</a></h3>
		    			<p>{{archive.description}}</p>
		    			<p><small>{{ archive.date }}</small></p>
		  			</div>
				</div>
			</div>
			{% endfor %}
"""