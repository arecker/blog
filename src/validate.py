"""validate site files"""

import logging
import re
import sys
import xml.etree.ElementTree

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


def is_valid_xml(content: str):
    """Check if the string is a valid XML document.

    >>> is_valid_xml('<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"></feed>')
    True

    >>> is_valid_xml('poop')
    False
    """
    try:
        xml.etree.ElementTree.fromstring(content)
        return True
    except xml.etree.ElementTree.ParseError:
        return False


def main(args):
    passed = True

    for f in ['feed.xml', 'sitemap.xml']:
        target = args.directory / 'www' / f
        with open(target, 'r') as f:
            if not is_valid_xml(f.read()):
                logger.warn('%s is not a valid XML!', target.name)
                passed = False
            else:
                logger.info('validated %s', target.name)

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
                # logger.warn('invalid href "%s" found in %s', href, html_file)
                # passed = False
                pass
            elif href.startswith('#'):
                # Check the document for the specified anchor
                expected = f'id="{href[1:]}"'
                if expected not in content:
                    logger.warn('nonexistent anchor "%s" found in %s', href,
                                html_file.name)
                    passed = False
            elif href.startswith('./'):
                # Check that the reference exists
                reference = args.directory / 'www' / href
                if not reference.is_file():
                    logger.warn('nonexistent href "%s" found in %s', href,
                                html_file)
                    passed = False
    logger.info('validated src and href attributes in %d file(s)',
                len(html_files))

    if not passed:
        logger.error('validation failed, there are problems to fix')
        sys.exit(1)
