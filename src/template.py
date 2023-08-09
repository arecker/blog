import collections
import jinja2
import pathlib


def render_template(template_name: str, context={}, templates_dir='./templates'):
    """
    Render a template into a string.
    """
    loader = jinja2.FileSystemLoader(searchpath=templates_dir)
    env = jinja2.Environment(loader=loader)
    template = env.get_template(template_name)
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
        env = jinja2.Environment(loader=jinja2.BaseLoader)
        with page.path.open('r') as f:
            content = env.from_string(f.read()).render(**context)
    else:
        # page isn't a template, so just read it
        with page.path.open('r') as f:
            content = f.read()

    # now, wrap that content in the base template
    context['content'] = content
    return render_template('base.html.j2', context=context)
