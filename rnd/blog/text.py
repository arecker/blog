import re


def plural(n, singular, plural=None):
    plural = plural or singular + 's'

    if n == 1:
        return f'{n} {singular}'

    return f'{n} {plural}'


def lines(subject):
    return list(filter(None, (l.strip() for l in subject.split('\n'))))


def extract_frontmatter(subject):
    pattern = r'^\s*---\n(.*?)---\s*'
    match = re.search(pattern, subject, flags=re.DOTALL)

    yaml = {}

    if match:
        data = match.group(1)
        subject = subject.replace(f'---\n{data}---\n', '', 1)
        return extract_yaml(data), subject
        
    return yaml, subject
    

def extract_yaml(subject):
    pattern = r'^\s?(.*):\s?(.*)$'
    return dict(re.findall(pattern, subject, flags=re.MULTILINE))