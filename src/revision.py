import argparse
import collections
import logging
import re

from . import paths, git


logger = logging.getLogger('blog')


Version = collections.namedtuple('Version', 'major minor patch')

r_version = re.compile(r'^v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$')
version_path = paths.join('VERSION')


def build_annotation(level):
    return f'new {level} version\n\n{git.shortlog_from_latest_tag()}'


def version_from_string(vstring):
    match = r_version.search(vstring)

    if not match:
        raise ValueError(f'"{vstring}" is not a valid version string')

    major, minor, patch = match.groups()

    return Version(major, minor, patch)


def version_to_string(version):
    return f'v{version.major}.{version.minor}.{version.patch}'


def make_next_version(current, level):
    values = {
        'major': int(current.major),
        'minor': int(current.minor),
        'patch': int(current.patch),
    }

    if level in ['major', 'minor']:
        values['patch'] = 0

    if level == 'major':
        values['minor'] = 0

    values[level] = values[level] + 1
    return Version(*[values[k] for k in ('major', 'minor', 'patch')])


argparser = argparse.ArgumentParser(prog='revision')
argparser.add_argument('level', choices=['major', 'minor', 'patch'])


def main():
    args = argparser.parse_args()
    with open(paths.join('VERSION'), 'r') as f:
        version_content = f.read().strip()

    current_v = version_from_string(version_content)
    logger.debug('current version is %s', current_v)

    next_v = make_next_version(current_v, args.level)
    logger.debug('next version is %s', next_v)

    old_version_string = version_to_string(current_v)
    new_version_string = version_to_string(next_v)
    logger.info(
        'incrementing %s version (%s -> %s)',
        args.level,
        old_version_string,
        new_version_string,
    )

    logger.debug('writing %s to %s', new_version_string, version_path)
    with open(version_path, 'w') as f:
        f.write(new_version_string)

    logger.debug('staging %s', version_path)
    git.stage(version_path)

    logger.debug('amending last commit')
    git.amend()

    logger.debug('creating tag %s', new_version_string)
    git.tag(new_version_string, annotation=build_annotation(args.level))

    logger.debug('pushing tree')
    git.push()

    logger.info('new tag created, current revision is %s', new_version_string)


if __name__ == '__main__':
    from .logging import configure_logging
    configure_logging()
    main()
