import os.path as Path
from os.path import join as Join
from os import listdir as ListDir
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import web


## Env Variables
root = Path.dirname(Path.realpath(__file__))


## Routing Config
urls = (
    '/', 'GetHome',
    '/archives', 'GetArchives',
    '/projects', 'GetProjects',
    '/friends', 'GetFriends',
    '/(.+)', 'GetPost'
)


## Controllers
class GetHome:
    """Returns latest post"""
    def GET(self):
        listOfPosts = GetListOfPosts()
        latestPost = listOfPosts[0]
        return DisplayHome(latestPost)


class GetPost:
    """Gets post by slug or 404"""
    def GET(self, slug):
        key = slug + '.html'
        listOfPosts = GetListOfPosts()
        indices = [i for i, s in enumerate(listOfPosts) if key in s]
        try:
            data = DisplayPost(listOfPosts[indices[0]])
        except:
            data = DisplayPage('404.html')
        return data


class GetArchives:
    """Gets Archives Page"""
    def GET(self):
        return DisplayPage('archives.html')


class GetProjects:
    """Gets Projects Page"""
    def GET(self):
        return DisplayPage('projects.html')


class GetFriends:
    """Gets Friends Page"""
    def GET(self):
        return DisplayPage('friends.html')


## Helpers
def GetListOfPosts():
    list = ListDir(Join(root, 'posts'))
    return list[::-1]

def DisplayHome(post):
    data = ""
    for fragment in [Frag("home_meta.html"), Frag("css.html"), Frag("header.html"), Join(root, 'posts', post), Frag("analytics.html")]:
        with open(fragment, "r") as page:
            data += page.read()
    return data

def DisplayPost(post):
    data = ""
    for fragment in [Meta(post), Frag("css.html"), Frag("header.html"), Join(root, 'posts', post), Frag("comments.html"), Frag("analytics.html")]:
        with open(fragment, "r") as page:
            data += page.read()
    return data

def DisplayPage(name):
    data = ""
    for fragment in [Meta(name), Frag("css.html"), Frag("header.html"), Join(root, 'pages', name), Frag("analytics.html")]:
        with open(fragment, "r") as page:
            data += page.read()
    return data

def Frag(name):
    return Join(root, 'fragments', name)

def Meta(name):
    return Join(root, 'metas', name)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

application = web.application(urls, globals()).wsgifunc()
