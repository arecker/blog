import re


def convert_emphasis(subject):
    pattern = r'_([A-Za-z0-9 ].*?)_'
    replace = r'<em>\1</em>'
    return re.sub(pattern, replace, subject, flags=re.DOTALL)
