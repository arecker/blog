import re


def convert_emphasis(subject):
    pattern = r'_(.*?)_'
    replace = r'<em>\1</em>'
    return re.sub(pattern, replace, subject, flags=re.DOTALL)


def convert_bold(subject):
    pattern = r'\*\*(.*?)\*\*'
    replace = r'<strong>\1</strong>'
    return re.sub(pattern, replace, subject, flags=re.DOTALL)


def convert_inline_links(subject):
    pattern = r'\[(.*?)\]\((.*?)\)'
    replace = r'<a href="\2">\1</a>'
    return re.sub(pattern, replace, subject, flags=re.DOTALL)


class LinkReplacer:
    inline_pattern = r'\[(.*?)\]\((.*?)\)'
    link_pattern = r'^\[(.*)\]\:\s?(.*)$'
    ref_pattern = r'\[(.*?)\]'

    def __init__(self, subject):
        self.subject = subject

    def extract(self):
        result = re.findall(self.link_pattern, self.subject, flags=re.MULTILINE)
        self.links = dict(result)

    def strip(self):
        if self.links:
            self.subject = re.sub(self.link_pattern, '', self.subject, flags=re.MULTILINE | re.DOTALL)

    def _replace_match(self, match):

        try:
            href = self.links[match.group(1)]
        except KeyError:  # TODO: a hack
            return match.group(0)
        content = match.group(1)
        return f'<a href="{href}">{content}</a>'

    def expand(self):
        self.subject = re.sub(
            self.ref_pattern,
            self._replace_match,
            self.subject,
            flags=re.DOTALL
        )


def convert_links(subject):
    replacer = LinkReplacer(subject)
    replacer.extract()
    replacer.strip()
    replacer.expand()
    return replacer.subject


def convert_headings(subject):
    headings = [
        (r'^##### (.*)$', r'<h5>\1</h5>'),
        (r'^#### (.*)$', r'<h4>\1</h4>'),
        (r'^### (.*)$', r'<h3>\1</h3>'),
        (r'^## (.*)$', r'<h2>\1</h2>'),
        (r'^# (.*)$', r'<h1>\1</h1>')
    ]

    for pattern, replace in headings:
        subject = re.sub(pattern, replace, subject, flags=re.MULTILINE)

    return subject


def convert(subject):
    subject = convert_links(subject)
    subject = convert_emphasis(subject)
    subject = convert_bold(subject)
    subject = convert_inline_links(subject)
    subject = convert_headings(subject)

    return subject
