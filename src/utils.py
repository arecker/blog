import logging
import logging.config
import os
import pathlib

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

    if paved != 0:
        logger.info('paved %d file(s) from webroot', paved)


def configure_logging(verbose=False):
    if verbose or os.environ.get('DEBUG'):
        level = 'DEBUG'
    else:
        level = 'INFO'

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(levelname)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': level,
                'propagate': True
            }
        }
    }
    logging.config.dictConfig(config)
