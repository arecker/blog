import re

from .yaml import parse_yaml


pattern = re.compile(r'<!--\s+blog:(?P<key>[A-Za-z-_\/]+)\s*:\s*(?P<value>.+?)\s*-->')
legacy_pattern = re.compile(r'^-{3}\n(.*?)\n-{3}\n', flags=re.DOTALL)


def parse_metadata(content, legacy=False):
    """
    Parses HTML metadata in comments.

    <!-- blog:key: value -->

    Or YAML frontmatter for legacy=True.
    """
    if legacy:
        if match := legacy_pattern.match(content):
            lines = match.groups()[0]
            data = parse_yaml(lines)
            leftovers = content[match.end():]
            return data, leftovers
        else:
            return {}, content
    else:
        return dict(pattern.findall(content))
