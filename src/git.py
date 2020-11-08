import re

from . import shell


r_status_short = re.compile(
    r'^(?P<glypph>\S+)\s+(?P<path>.*)$',
    flags=re.MULTILINE
)


def new_files():
    result = shell.run('git status --short')
    for glyph, path in r_status_short.findall(result.stdout):
        if glyph != 'D':
            yield path


def stage(filepath):
    shell.run(f'git add {filepath}')
