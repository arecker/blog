import pathlib
import logging

logger = logging.getLogger(__name__)


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

    redirects_file = www_dir / '_redirects'

    if redirects_file.is_file():
        redirects_file.unlink()
        paved += 1
        logger.debug('removed %s', redirects_file)

    if paved != 0:
        logger.info('paved %d file(s) from webroot', paved)
