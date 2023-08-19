import pathlib


def pave_webroot():
    """
    Delete all old generated files from webroot

    Returns the number of old files detected and destroyed.
    """

    webroot = pathlib.Path('./www')

    old_files = []
    old_files += list(webroot.glob('*.html'))
    old_files += list(webroot.glob('*.xml'))

    for target in old_files:
        target.unlink()

    return len(old_files)
