import math
import os
import pathlib
import logging

logger = logging.getLogger(__name__)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return '{} {}'.format(s, size_name[i])


def pave_webroot(www_dir=''):
    www_dir = pathlib.Path(www_dir)

    paved = 0

    html_files = list(www_dir.glob('*.html'))
    if html_files:
        [f.unlink() for f in html_files]
        paved += len(html_files)
        logger.debug('paved %d HTML file(s) from %s', len(html_files), www_dir)

    xml_files = list(www_dir.glob('*.xml'))
    if xml_files:
        [f.unlink() for f in xml_files]
        paved += len(xml_files)
        logger.debug('paved %d XML file(s) from %s', len(xml_files), www_dir)

    if paved != 0:
        logger.info('paved %d file(s) from webroot', paved)
