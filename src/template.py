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


def render_page(page, site, entries, pages, pages_dir='./pages'):
    """
    Render a page into a string.
    """
    # make context
    context = {
        'page': page,
        'site': site,
        'entries': entries,
        'pages': pages,
    }

    try:
        context['latest'] = entries[0]
    except IndexError:
        context['latest'] = None

    # render sub page
    if hasattr(page, 'content'):  # skip rendering inner page
        content = page.content
    else:  # render inner page
        loader = jinja2.FileSystemLoader(searchpath=pages_dir)
        env = jinja2.Environment(loader=loader)
        template = env.get_template(page.template_name)
        content = template.render(**context)

    # now, wrap that content in the base template
    context['content'] = content
    return render_template('base.html.j2', context=context)
