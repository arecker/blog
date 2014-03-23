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
    '/friends', 'GetFriends',
    '/(.+)', 'GetPost'
)


## Controllers
class GetHome:
    """Returns latest post"""
    def GET(self):
        return DisplayPage(Join(root, 'pages', 'skel.html'))


class GetPost:
    """Gets post by slug or 404"""
    def GET(self, slug):
        key = slug + '.html'

        #if key in GetListOfPosts():
        #    data = DisplayPage(Join(root, 'posts', key))
        #else:
        #    data = DisplayPage(Join(root, 'pages', '404.html'))
        #return data
        listOfPosts = GetListOfPosts()
        indices = [i for i, s in enumerate(listOfPosts) if key in s]
        try:
            data = DisplayPage(Join(root, 'posts', listOfPosts[indices[0]]))
        except:
            data = DisplayPage(Join(root, 'pages', '404.html'))
        return data


class GetArchives:
    """Gets Archives Page"""
    def GET(self):
        return DisplayPage(Join(root, 'pages', 'archives.html'))


class GetFriends:
    """Gets Friends Page"""
    def GET(self):
        return DisplayPage(Join(root, 'pages', 'friends.html'))


## Helpers
def GetListOfPosts():
    return ListDir(Join(root, 'posts'))

def DisplayPage(path):
    with open(path, "r") as page:
        return page.read()

def GetLatestPost():
    pass

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

application = web.application(urls, globals()).wsgifunc()
