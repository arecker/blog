import jinja2


template_loader = jinja2.FileSystemLoader(searchpath='./templates')
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_name: str, context={}):
    """
    Render a template into a string.
    """
    template = template_env.get_template(template_name)
    return template.render(**context)
