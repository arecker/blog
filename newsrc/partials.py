import decorator


@decorator.decorator
def partial(func, level=0, *args, **kwargs):
    result = func(*args, **kwargs).strip()
    indent = ''.join([' ' * level])
    commented = '''
<!-- partial: {name} -->
{result}
<!-- end: {name} -->
'''.format(name=func.__name__, result=result).strip()
    indented = '\n'.join([indent + line for line in commented.splitlines()])
    return indented + '\n'


@partial(level=4)
def header(title='Title', description='Description'):
    return '''
<header>
  <h1 class="title">{title}</h1>
  <h2 class="subtitle">{description}</h2>
</header>
'''.format(title=title, description=description)


@partial(level=4)
def banner(filename='', href=None):
    if not filename:
        return ''

    href = href or f'/images/banners/{filename}'

    return '''
<figure>
  <a href="{href}">
    <img alt="banner" src="/images/banners/{filename}" />
  </a>
</figure>
'''.format(filename=filename, href=href)


@partial(level=4)
def footer(year='',
           author='',
           timestamp='',
           git_commit='',
           git_commit_short='',
           git_commit_summary=''):
    return '''
<footer>
  <small>Last Updated: {timestamp}</small>
  <small>Last Change: <span>{git_commit_summary} (<a href="https://github.com/arecker/blog/commit/{git_commit}">{git_commit_short}</a>)</span></small>
  <small>&copy; Copyright {year} {author}</small>
</footer>
'''.format(year=year,
           author=author,
           timestamp=timestamp,
           git_commit='',
           git_commit_short='',
           git_commit_summary='')


@partial(level=8)
def navlist(pagelist=[]):
    tmpl = '<a href="/{page}">{page}</a>'
    elements = [tmpl.format(page=page) for page in pagelist]
    return '\n'.join(elements)
