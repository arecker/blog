import collections
import re


Version = collections.namedtuple('Version', 'major minor patch')

r_version = re.compile(r'^v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$')


def version_from_string(vstring):
    match = r_version.search(vstring)

    if not match:
        raise ValueError(f'"{vstring}" is not a valid version string')

    major, minor, patch = match.groups(1, 2, 3)

    return Version(major, minor, patch)


def main():
    pass


if __name__ == '__main__':
    from .logging import configure_logging
    configure_logging()
    main()
