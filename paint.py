import json
from os.path import splitext, join


class Globals:
    def __init__(self):
        filepath = splitext(__file__)[0]
        self.pages = join(filepath, '..', 'content', 'pages.json')


class CacheWriter:
    def __init__(self):
        # Read in json for site content
        data = json.load(open())