import os
import re


here = os.path.dirname(os.path.abspath(__file__))

r_figure = re.compile(
    r'''{% include figure\.html\s+filename=['"]?(?P<filename>\S*)['"]\s+%}''',
    flags=re.DOTALL
)
r_figure_with_caption = re.compile(
    r'''{% include figure\.html\s+filename=['"]?(?P<filename>\S*)['"]\s+caption=['"]?(?P<caption>.*?)['"]?\s?%}''',
    flags=re.DOTALL
)


def entries():
    entries_dir = os.path.abspath(os.path.join(here, '../entries'))
    return [os.path.join(entries_dir, entry) for entry in os.listdir(entries_dir)]


def old_posts():
    old_dir = os.path.abspath(os.path.join(here, '../pages/old'))
    return [os.path.join(old_dir, entry) for entry in os.listdir(old_dir)]


def sub_figure(match):
    src = '/images/' + match.group('filename')
    alt = re.sub(r'[-_/]', ' ', os.path.splitext(match.group('filename'))[0])
    html = '''
<figure>
  <a href="{src}">
    <img alt="{alt}" src="{src}"/>
  </a>
</figure>'''.format(alt=alt, src=src).strip()
    return html


def sub_figure_with_caption(match):
    src = '/images/' + match.group('filename')
    alt = re.sub(r'[-_/]', ' ', os.path.splitext(match.group('filename'))[0])
    caption = match.group('caption')
    html = '''
<figure>
  <a href="{src}">
    <img alt="{alt}" src="{src}"/>
  </a>
  <figcaption>
    <p>{caption}</p>
  </figcaption>
</figure>'''.format(alt=alt, src=src, caption=caption).strip()
    return html


def main():
    for entry in entries() + old_posts():
        with open(entry) as f:
            before = f.read()

        after = r_figure.sub(sub_figure, before)
        after = r_figure_with_caption.sub(sub_figure_with_caption, after)
        if before == after:
            print('no change: {}'.format(entry))
        else:
            print('change   : {}'.format(entry))

        with open(entry, 'w') as f:
            f.write(after)



if __name__ == '__main__':
    main()
