import collections
import configparser
import pathlib


Config = collections.namedtuple('Config', [
    'site',
])

SiteConfig = collections.namedtuple('SiteConfig', [
    'email',
    'name',
    'subtitle',
    'template',
    'title',
    'url',
    'www',
])

def load(config_path):
    config = configparser.ConfigParser()
    config_path = pathlib.Path(config_path)
    config.read(str(config_path))

    kwargs = dict(config['site'].items())
    site_config = SiteConfig(**kwargs)

    return Config(
        site=site_config,
    )

if __name__ == '__main__':
    load('../blog.conf')
