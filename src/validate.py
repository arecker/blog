"""validate site files"""

import logging
import re
import sys
import xml.etree.ElementTree

from . import utils

logger = logging.getLogger(__name__)


def extract_refs(content: str):
    """Extract href and src patterns from a string.
    
    >>> example = 'A link to <href="google.com">google</a>.'
    >>> extract_refs(example)
    ['google.com']

    >>> example = '<link href="./assets/site.css" rel="stylesheet"/>'
    >>> extract_refs(example)
    ['./assets/site.css']

    >>> example = '<img src="./images/banners/2022-02-18.jpg" alt="banner image for latest post"/>'
    >>> extract_refs(example)
    ['./images/banners/2022-02-18.jpg']
    """
    r_href = re.compile(r'(?:href|src)=\"(.*?)\"')
    return r_href.findall(content)

def main(args):
    passed = True
    
    for f in ['feed.xml', 'sitemap.xml']:
        target = args.directory / 'www' / f
        try:
            xml.etree.ElementTree.parse(target)
            logger.info('validated %s', target.name)
        except xml.etree.ElementTree.ParseError:
            logger.warn('%s is not a valid XML!', target.name)
            passed = False

    html_files = list(args.directory.glob('www/*.html'))
    assert html_files, "No HTML files found, did you build the project first?"

    for html_file in html_files:
        with open(html_file, 'r') as f:
            content = f.read()

        for href in extract_refs(content):
            if href.startswith('/'):
                # TODO: turn this on after fixing all the entries
                # Links shouldn't start with a slash, because it
                # breaks local browsing without a webserver.
                # logger.warn('invalid href "%s" found in %s', href, utils.prettify_path(html_file))
                # passed = False
                pass
            elif href.startswith('#'):
                # Check the document for the specified anchor
                expected = f'id="{href[1:]}"'
                if expected not in content:
                    logger.warn('nonexistent anchor "%s" found in %s', href, html_file.name)
                    passed = False
            elif href.startswith('./'):
                # Check that the reference exists
                reference = args.directory / 'www' / href
                if not reference.is_file():
                    logger.warn('nonexistent href "%s" found in %s', href, utils.prettify_path(html_file))
                    passed = False

    logger.info('validated src and href attributes in %d file(s)', len(html_files))

    if not passed:
        logger.error('validation failed, there are problems to fix')
        sys.exit(1)
