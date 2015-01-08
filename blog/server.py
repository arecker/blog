import os
import flask
from core import Config


class WebServer:
    def __init__(self, address='127.0.0.1'):
        self.config = Config()
        self.app = flask.Flask(__name__)
        self.app.static_folder = self.config.static
        self.app.debug = True
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/<slug>/', 'slug', self.get_slug)
        self.app.run(host=address)


    def index(self):
        return self.read_file('index.html', 'text/html')


    def get_slug(self, slug):
        try:
            return self.read_file(slug, mimetype="text/html")
        except IOError:
            try:
                return self.read_file(os.path.join(slug, 'index.html'), 'text/html')
            except IOError:
                return self.read_file(os.path.join(slug, 'index.xml'), 'text/xml')


    def read_file(self, target, mimetype):
        with open(os.path.join(self.config.public, target)) as file:
            return flask.Response(file.read(), mimetype)