import glob
import os
import re


here = os.path.dirname(os.path.abspath(__file__))
pattern = re.compile(r'^---\n.*?---\n[^\S]*', flags=re.DOTALL)


def join(path):
    root = os.path.abspath(os.path.join(here, '..'))
    return os.path.join(root, path)


def list_entries():
    return glob.glob(join('entries/*'))


def list_banners():
    return glob.glob(join('images/banners/*'))


def make_snippet(filename):
    return '''
<figure>
  <a href="/images/banners/{filename}">
    <img alt="banner" src="/images/banners/{filename}"/>
  </a>
</figure>
'''.strip().format(filename=filename)


def main():
    banners = dict([
        (os.path.splitext(os.path.basename(f))[0], os.path.basename(f))
        for f
        in list_banners()
    ])
    for entry in list_entries():
        key = os.path.splitext(os.path.basename(entry))[0]
        try:
            banner = banners[key]
            snippet = make_snippet(banner)
            with open(entry) as f:
                before = f.read()

            match = pattern.search(before)
            after = ''.join([
                before[0:match.end()],
                snippet + '\n\n',
                before[match.end():]
            ])

            with open(entry, 'w') as f:
                f.write(after)
        except KeyError:
            continue


if __name__ == '__main__':
    main()
