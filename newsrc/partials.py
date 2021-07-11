import decorator

from newsrc import git


@decorator.decorator
def partial(func, level=0, *args, **kwargs):
    result = func(*args, **kwargs).strip()
    indent = ''.join([' ' * level])
    commented = '''
<!-- partial: {name} -->
{result}
<!-- end: {name} -->
'''.strip().format(name=func.__name__, result=result)
    indented = '\n'.join([indent + line for line in commented.splitlines()])
    return indented


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
           git_commit=git.head(),
           git_commit_short=git.short_head(),
           git_commit_summary=git.head_summary())


@partial(level=8)
def nav(pagelist=[]):
    tmpl = '<a href="/{page}">{page}</a>'
    elements = [tmpl.format(page=page) for page in pagelist]
    return '\n'.join(elements)


@partial(level=6)
def breadcrumbs(permalink=''):
    if permalink == 'index.html':
        return '''
<a href="/">index.html</a>
'''.strip()

    return '''
<a href="/">index.html</a>
<span>/</span>
<span>{permalink}</span>
'''.format(permalink=permalink).strip()


@partial(level=6)
def pagination(next_page=None, previous_page=None):
    elements = []
    if next_page:
        elements.append(
            '<a class="float-right" href="/{next_page}">{next_page} ⟶</a>'.
            format(next_page=next_page))

    if previous_page:
        elements.append(
            '<a class="float-left" href="/{previous_page}">⟵ {previous_page}</a>'
            .format(previous_page=previous_page))

    return '\n'.join(elements)


@partial(level=8)
def latest(entry):
    if entry.banner_filename:
        return '''
<figure>
  <a href="/{permalink}">
    <img alt="{description}" src="{banner_relative_url}" />
  </a>
  <figcaption>
    <a href="/{permalink}">
      <h2>{title}</h2>
    </a>
    <p>{description}</p>
  </figcaption>
</figure>'''.strip().format(permalink=entry.permalink,
                            title=entry.title,
                            description=entry.description,
                            banner_relative_url=entry.banner_relative_url)
    else:
        return '''
<a href="/{permalink}">
  <h2>{title}</h2>
</a>
<p>{description}</p>'''.strip().format(permalink=entry.permalink,
                                       title=entry.title,
                                       description=entry.description)


@partial(level=4)
def entries_table(entries=[]):
    elements = ['<table>']

    for entry in entries:
        row = '''  <tr>
    <td>
      <a href="/{permalink}">{permalink}</a>
    </td>
    <td>{description}</td>
  </tr>'''.format(permalink=entry.permalink, description=entry.description)
        elements.append(row)

    elements.append('</table>')

    return '\n'.join(elements)
