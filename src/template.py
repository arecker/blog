import collections
import jinja2
import pathlib


template_loader = jinja2.FileSystemLoader(searchpath='./templates')
template_env = jinja2.Environment(loader=template_loader)


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
