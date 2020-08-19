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


def convert_links(subject):
    link_pattern = r'^\[(.*)\]\:\s?(.*)$'

    # extract links
    links = dict(re.findall(link_pattern, subject, flags=re.MULTILINE))

    # strip links
    if links:
        subject = re.sub(link_pattern, '', subject, flags=re.MULTILINE)

    # expand refs
    ref_pattern = r'\s\[(.*?)\]'
    for ref in re.findall(ref_pattern, subject, flags=re.DOTALL):
        pass

    return subject


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
    subject = convert_emphasis(subject)
    subject = convert_bold(subject)
    subject = convert_inline_links(subject)
    subject = convert_headings(subject)

    return subject
