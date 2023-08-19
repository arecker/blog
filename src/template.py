import logging
import pathlib
import xml.etree.ElementTree

import jinja2


logger = logging.getLogger(__name__)


def embed(obj):
    klass = type(obj).__name__

    if klass == 'Image':
        return render_template(
            'figure.html.j2',
            context={
                'href': obj.href,
                'src': obj.href,
                'alt': obj.title,
            }
        )

    if klass == 'Page':
        caption = f'<p><a href="./{obj.filename}">{obj.description}</a></p>'
        return render_template(
            'figure.html.j2',
            context={
                'href': f'./{obj.filename}',
                'src': f'./images/banners/{obj.banner}',
                'alt': obj.title,
                'caption': caption
            }
        )

    raise TypeError(f'cannot embed type {klass}!')


template_loader = jinja2.FileSystemLoader(searchpath='./templates')
template_env = jinja2.Environment(loader=template_loader)
template_env.filters['embed'] = embed


def prettify_xml(content: str) -> str:
    """
    Returns a prettified version of the XML document in `content` as a
    `str`.

    Warning: this raises a `xml.etree.ElementTree.ParseError` if there
    is *anything* invalid in the document, and - being XML - it's kind
    of picky.
    """
    tree = xml.etree.ElementTree.fromstring(content)
    xml.etree.ElementTree.indent(tree)
    content = xml.etree.ElementTree.tostring(
        tree, encoding='utf8', method='html').decode('utf-8')
    return content


def write_page(page, context={}):
    # first render the conent
    content = render_page(page, context=context)
    content = content.strip()

    # prettify it
    if page.filename.endswith('.html'):
        content = '\n'.join(content.splitlines()[1:])  # remove doctype
        content = content.replace('&', '&amp;')  # clean up chars
        try:
            content = prettify_xml(content)
            content = '<!doctype html>\n' + content  # add doctype back
        except xml.etree.ElementTree.ParseError as e:
            msg = 'invalid XML on row %d, col %d'
            msg = 'error writing %s: ' + msg
            logger.warn(
                msg,
                page.filename,
                e.position[0] + 1, e.position[1]
            )

    # now write it to the webroot
    target = pathlib.Path(f'www/{page.filename}')
    with target.open('w') as f:
        f.write(content)


def render_template(template_name: str, context={}):
    """
    Render a template into a string.
    """
    template = template_env.get_template(template_name)
    return template.render(**context)


def render_page(page, context={}, pages_dir='./pages'):
    """
    Render a page into a string.
    """

    # add current page to context
    context = context._asdict()
    context['page'] = page

    if page.path.name.endswith('.j2'):
        # page is a template, so render it
        with page.path.open('r') as f:
            content = template_env.from_string(f.read()).render(**context)
    else:
        # page isn't a template, so just read it
        with page.path.open('r') as f:
            content = f.read()

    # indent the content so the HTML looks purty
    content = '\n'.join(['      ' + row for row in content.split('\n')])

    # now, wrap that content in the base template
    context['content'] = content
    return render_template('base.html.j2', context=context)
