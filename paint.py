import json
from os.path import splitext, join, dirname
from jinja2 import Environment, FileSystemLoader


class ConfigurationModel:
    def __init__(self):
        filepath = splitext(__file__)[0]
        self.pages = join(dirname(filepath), 'content', 'pages.json')
        self.templates = join(dirname(filepath), 'templates')
        self.page_cache = join(dirname(filepath), 'cache', 'pages')


class Headline:
    def __init__(self, title, image, caption, link):
        self.title = title
        self.image = image
        self.caption = caption
        self.link = link


class CacheWriter:
    def __init__(self):
        # Get Config Object
        self.config = ConfigurationModel()

        # Read in json for site content
        data = json.load(open(self.config.pages))
        self.Home = data["Home"]


    def WriteHomePage(self):
        headlines = []
        for headline in self.Home["Headlines"]:
            headlines.append(
                Headline(
                    title = headline["title"],
                    image = headline["image"],
                    caption = headline["caption"],
                    link = headline["link"]
                )
            )
        self.WriteOutToTemplate(template_name='home.html', collection=headlines)


    def WriteOutToTemplate(self, template_name, collection):
        ENV = Environment(loader=FileSystemLoader(self.config.templates))
        template = ENV.get_template(template_name)
        with open(join(self.config.page_cache, template_name), 'wb') as file:
            file.write(template.render(
                collection = collection
            ))


if __name__ == '__main__':
    cw = CacheWriter()
    cw.WriteHomePage()

