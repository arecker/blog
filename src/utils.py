import pathlib


def pave_webroot() -> int:
    """
    Delete all old generated files from webroot

    Returns the number of old files detected and destroyed.  This is
    so you have something interesting to log.

    ```python
    logger.info('paved %d old file(s) from webroot!', src.pave_webroot())
    ```
    """

    webroot = pathlib.Path('./www')

    old_files = []
    old_files += list(webroot.glob('*.html'))
    old_files += list(webroot.glob('*.txt'))
    old_files += list(webroot.glob('*.xml'))
    old_files += list(webroot.glob('api/*.html'))
    old_files += list(webroot.glob('api/*.js'))

    for target in old_files:
        target.unlink()

    return len(old_files)
