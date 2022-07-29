import logging
import pathlib
import re
import collections

logger = logging.getLogger(__name__)

Reference = collections.namedtuple('Reference',
                                   ['attribute', 'filename', 'path'])


def extract_references(dir_www):
    r_reference = re.compile(r'(?P<attribute>href|src)=".\/(?P<path>.*?)"',
                             re.DOTALL)

    for item in pathlib.Path(dir_www).glob('*.html'):
        with item.open('r') as f:
            for match in r_reference.finditer(f.read()):
                reference = Reference(filename=item.name,
                                      attribute=match.group('attribute'),
                                      path=match.group('path'))
                yield reference


def walk_assets(dir_www):
    dir_www = pathlib.Path(dir_www)

    for item in dir_www.glob('images/**/*.*'):
        yield item.relative_to(dir_www)

    for item in dir_www.glob('vids/**/*.*'):
        yield item.relative_to(dir_www)

    for item in dir_www.glob('assets/**/*.*'):
        yield item.relative_to(dir_www)

    for item in dir_www.glob('audio/**/*.*'):
        yield item.relative_to(dir_www)


def validate_website(dir_www: str | pathlib.Path):
    logger.info('validating site files in %s', dir_www)

    references = [r for r in extract_references(dir_www)]

    for reference in references:
        if not (pathlib.Path(dir_www) / reference.path).is_file():
            logger.warn('WARNING - %s %s="./%s" - cannot find resource',
                        reference.filename, reference.attribute,
                        reference.path)

    assets = [a for a in walk_assets(dir_www)]

    for asset in assets:
        try:
            next((r for r in references if r.path == str(asset)))
        except StopIteration:
            logger.warn('WARNING - %s is not referenced in any site files',
                        asset)
