import logging
import pathlib

from .images import scan_images, fetch_images

logger = logging.getLogger(__name__)


def fixup_project(entries_dir='', www_dir=''):
    entries_dir = pathlib.Path(entries_dir)
    entries = list(entries_dir.glob('*.html'))
    total = len(entries)
    logger.debug('fixing up %d entries in %s', total, entries_dir)

    for i, entry in enumerate(entries):
        with entry.open('r') as f:
            content = f.read()
            if '--> <!--' in content:
                logger.warning('%s: found misaligned metadata', entry.name)

        if i % 100 == 0:
            logger.info('scanned entries %d of %d', i, total)

    for image in fetch_images(www_directory=www_dir):
        found = False
        for entry in entries:
            with entry.open('r') as f:
                if image.name in f.read():
                    found = True
                    break
        if not found:
            image.unlink()
            logger.warn('deleted unused image %s', image)

    # scan_images(dir_www=www_dir)
