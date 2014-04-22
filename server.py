from os.path import join, splitext, abspath
from flask import Flask
app = Flask(__name__)


### Global Variables
filepath, extension = splitext(__file__)
PAGES = abspath(join(filepath, '..', 'content/pages'))
POSTS = abspath(join(filepath, '..', 'content/posts'))
CACHE = abspath(join(filepath, '..', 'cache'))
STATIC = abspath(join(filepath, '..', 'static'))


### Controllers
@app.route("/")
def GetHome():
    home_page = open(join(CACHE, 'pages/home.html'), 'r').read()
    return home_page


@app.route("/archives/")
def GetArchives():
    archives_page = open(join(CACHE, 'pages/archives.html'), 'r').read()
    return archives_page


@app.route("/projects/")
def GetProjects():
    projects_page = open(join(CACHE, 'pages/projects.html'), 'r').read()
    return projects_page


@app.route("/friends/")
def GetFriends():
    friends_page = open(join(CACHE, 'pages/friends.html'), 'r').read()
    return friends_page


@app.route("/sitemap/")
def GetSiteMap():
    sitemap = open(join(STATIC, 'sitemap.xml'), 'r').read()
    return sitemap


@app.route("/<slug>/")
def GetPost(slug):
    try:
        post = open(join(CACHE, 'posts/' + slug + '.html'), 'r').read()
        return post
    except:
        missing_page = open(join(CACHE, 'pages/404.html'), 'r').read()
        return missing_page


### Init App
if __name__ == "__main__":
    app.run()
