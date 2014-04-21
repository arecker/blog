from os.path import join, splitext, abspath
from flask import Flask
app = Flask(__name__)

### Global Variables
filepath, extension = splitext(__file__)
PAGES = abspath(join(filepath, '..', 'Content/pages'))
POSTS = abspath(join(filepath, '..', 'Content/posts'))
CACHE = abspath(join(filepath, '..', 'Cache'))

@app.route("/")
def GetHome():
    home_page = open(join(CACHE, 'homepage-cache.html'), 'r').read()
    return home_page

@app.route("/archives")
def GetArchives():
    archives_page = open(join(CACHE, 'archives-cache.html'), 'r').read()
    return archives_page

if __name__ == "__main__":
    app.run()