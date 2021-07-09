import functools
import decorator


@decorator.decorator
def partial(func, level=0, *args, **kwargs):
    result = func(*args, **kwargs).strip()
    indent = ''.join([' ' * level])
    commented = '''
<!-- begin: {name} -->
{result}
<!-- end: {name} -->
'''.format(name=func.__name__, result=result, indent=indent).strip()
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
