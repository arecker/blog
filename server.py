from os.path import join
from cache import ConfigurationModel
from flask import Flask, Response
app = Flask(__name__)
config = ConfigurationModel()


### Controllers
@app.route("/")
def GetHome():
    home_page = open(join(config.cache, 'home.html'), 'r').read()
    return home_page


@app.route("/archives/")
def GetArchives():
    archives_page = open(join(config.cache, 'archives.html'), 'r').read()
    return archives_page


@app.route("/projects/")
def GetProjects():
    projects_page = open(join(config.cache, 'projects.html'), 'r').read()
    return projects_page


@app.route("/friends/")
def GetFriends():
    friends_page = open(join(config.cache, 'friends.html'), 'r').read()
    return friends_page


@app.route("/sitemap.xml")
def GetSiteMap():
    xml = open(join(config.static, 'sitemap.xml'), 'r').read()
    return Response(xml, mimetype='text/xml')


@app.route("/robots.txt")
def GetRobots():
    robots = open(join(config.static, 'robots.txt'), 'r').read()
    return Response(robots, mimetype='text')


@app.route("/<slug>/")
def GetPost(slug):
    try:
        post = open(join(config.cache, slug + '.html'), 'r').read()
        return post
    except:
        missing_page = open(join(config.cache, '404.html'), 'r').read()
        return missing_page


### Init App
if __name__ == "__main__":
    app.run()
