import collections
import logging
import pathlib

from .. import lib

logger = logging.getLogger(__name__)


def each_word_in_file(target):
    with target.open('r') as f:
        for line in f.readlines():
            for word in line.strip().split():
                yield word.lower().strip()


def scan_entry_for_swears(entry, args, swear_jar):
    target = pathlib.Path(args.dir_entries) / entry.filename

    for word in each_word_in_file(target):
        try:
            swear_jar[word] += 1
        except KeyError:
            pass

    return swear_jar


@lib.register_page(filename='swears.html', title='Swear Jar', description='my online swear jar', banner='mugshot.jpg')
def render(renderer=None, args=None, entries=[], pages=[]):
    swears = (
        'ass',
        'bitch',
        'dammit',
        'damn',
        'dick',
        'fuck',
        'hell',
        'shit',
    )
    
    swear_jar = dict([(key, 0) for key in swears])

    for entry in entries:
        swear_jar = scan_entry_for_swears(entry, args, swear_jar)

    # sort swears by occurance
    swear_jar = sorted(swear_jar.items(), key=lambda t: int(t[1]), reverse=True)

    with renderer.wrapping_block('table'):
        for swear, count in swear_jar:
            with renderer.wrapping_block('tr'):
                renderer.block('td', contents=swear)
                renderer.block('td', contents=str(count))

    return renderer.text
