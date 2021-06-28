import re


PATTERN = re.compile(r'^-{3}\n(?P<region>.*?)-{3}\n{2}(?P<body>.*)$', re.DOTALL)
ITEM_PATTERN = re.compile(r'^(.*?)\s*:\s*(.*)$', re.MULTILINE)


def parse_frontmatter(content):
    """
    Parses a string containing frontmatter into data.  Returns the
    data and the "leftovers".
    """

    if match := PATTERN.match(content):
        region, leftovers = match.groups()
        data = dict(ITEM_PATTERN.findall(region))
    else:
        data, leftovers = {}, content

    return data, leftovers
