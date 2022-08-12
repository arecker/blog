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

    patterns = [
        'assets/**/*.*',
        'audio/**/*.*',
        'images/**/*.*',
        'vids/**/*.*',
    ]

    for pattern in patterns:
        for item in dir_www.glob(pattern):
            yield item.relative_to(dir_www)


def validate_website(dir_www):
    logger.info('validating site files in %s', dir_www)

    references = [r for r in extract_references(dir_www)]

    for reference in references:
        if not (pathlib.Path(dir_www) / reference.path).is_file():
            logger.warn('WARNING - %s %s="./%s" - cannot find resource',
                        reference.filename, reference.attribute,
                        reference.path)

    assets = [a for a in walk_assets(dir_www)]
    referenced_paths = set([str(r.path) for r in references])

    for asset in assets:
        if str(asset) not in referenced_paths:
            logger.warn('WARNING - %s is not referenced in any site files',
                        asset)
