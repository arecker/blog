import re

line_pattern = re.compile(r'^(?P<key>[A-Za-z0-9]*)\s*:\s*(?P<value>.*)$', re.MULTILINE)


def parse_yaml(content):
    matches = line_pattern.findall(content)
    return dict(matches)
