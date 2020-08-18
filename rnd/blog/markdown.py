import re


def convert_emphasis(subject):
    pattern = r'_(.*?)_'
    replace = r'<em>\1</em>'
    return re.sub(pattern, replace, subject, flags=re.DOTALL)


def convert_bold(subject):
    pattern = r'\*\*(.*?)\*\*'
    replace = r'<strong>\1</strong>'
    return re.sub(pattern, replace, subject, flags=re.DOTALL)


def convert_headings(subject):
    headings = [
        (r'##### (.*)', r'<h5>\1</h5>'),
        (r'#### (.*)', r'<h4>\1</h4>'),
        (r'### (.*)', r'<h3>\1</h3>'),
        (r'## (.*)', r'<h2>\1</h2>'),
        (r'# (.*)', r'<h1>\1</h1>')
    ]

    for pattern, replace in headings:
        subject = re.sub(pattern, replace, subject)

    return subject


def convert(subject):
    subject = convert_emphasis(subject)
    subject = convert_bold(subject)
    subject = convert_headings(subject)

    return subject
