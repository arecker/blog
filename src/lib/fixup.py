import logging
import pathlib
import re

from .images import scan_images, fetch_images, is_banner

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

        new_content = re.sub(r'(href|src)="\/(.*?)"', r'\1="./\2"', content)
        if new_content != content:
            with entry.open('w') as f:
                f.write(new_content)
            logger.warn('%s: removed absolute href to local asset', entry)

        if i % 100 == 0:
            logger.info('checking entry content %d of %d', i + 1, total)

    images = fetch_images(www_directory=www_dir)
    total = len(images)
    for i, image in enumerate(images):
        # TODO: check banners too
        if is_banner(image):
            continue

        found = False
        for entry in entries:
            with entry.open('r') as f:
                if image.name in f.read():
                    found = True
                    break
        if not found:
            image.unlink()
            logger.warn('deleted unused image %s', image)

        if i % 100 == 0:
            logger.info('checking for unused images %d of %d', i + 1, total)

    scan_images(dir_www=www_dir)
