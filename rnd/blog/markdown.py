import re


class Problem(BaseException):
    pass


def convert_emphasis(subject):
    pattern = r'(^|\b)_(?P<content>.*?)_($|\b)'
    replace = r'<em>\2</em>'
    return re.sub(pattern, replace, subject, flags=re.DOTALL)


def convert_bold(subject):
    pattern = r'\*\*(.*?)\*\*'
    replace = r'<strong>\1</strong>'
    return re.sub(pattern, replace, subject, flags=re.DOTALL)


class LinkReplacer:
    inline_pattern = r'\[(.*?)\]\((.*?)\)'
    link_pattern = r'^\s*\[(.*)\]\:\s?(.*)$'
    ref_pattern = r'\\?\[(.*?)\\?\]'
    escaped_ref_pattern = r'\\\[(.*?)\\\]'

    def __init__(self, subject):
        self.subject = subject

    def extract(self):
        result = re.findall(self.link_pattern, self.subject, flags=re.MULTILINE)
        self.links = dict(result)

    def strip(self):
        if self.links:
            self.subject = re.sub(self.link_pattern, '', self.subject, flags=re.MULTILINE | re.DOTALL)

    def _replace_match(self, match):
        if re.match(self.escaped_ref_pattern, match.group(0), flags=re.DOTALL):
            # escaped brackets, e.g. "A \[sort of\] quote."
            return f'[{match.group(1)}]'
        try:
            key = match.group(1).replace('\n', ' ')
            href = self.links[key]
        except KeyError:
            raise Problem(f'unknown link ref: [{key}]')
        content = match.group(1)
        return f'<a href="{href}">{content}</a>'

    def _expand_inline(self):
        replace = r'<a href="\2">\1</a>'
        return re.sub(self.inline_pattern, replace, self.subject, flags=re.DOTALL)

    def expand(self):
        self.subject = self._expand_inline()
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


def convert_code(subject):
    pattern = r'`{3}(?P<lang>[\S]+)?\n(?P<content>.*?)`{3}'
    replace = r'<pre class="\1">\n\2</pre>'
    return re.sub(pattern, replace, subject, flags=re.DOTALL)


def convert_paragraphs(subject):
    pattern = r'(.+?)(\n\n|\n$|$)'
    replace = r'<p>\1</p>\2'
    return re.sub(pattern, replace, subject, flags=re.DOTALL)


def convert(subject):
    subject = convert_code(subject)
    subject = convert_paragraphs(subject)
    subject = convert_links(subject)
    subject = convert_emphasis(subject)
    subject = convert_bold(subject)
    subject = convert_headings(subject)

    return subject
