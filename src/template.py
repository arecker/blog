import pathlib

import jinja2


_TEMPLATES = {}


def load(template_path: str) -> jinja2.Template:
    """Load a template by filepath."""

    template_path = pathlib.Path(template_path)

    # check the cache
    if str(template_path) in _TEMPLATES.keys():
        # sweet!  return cached template
        return _TEMPLATES[str(template_path)]

    parent = template_path.parent
    loader = jinja2.FileSystemLoader(searchpath=str(parent))
    env = jinja2.Environment(loader=loader)
    template = env.get_template(template_path.name)

    # now place it in the cache and return it
    _TEMPLATES[str(template_path)] = template
    return template


def render(template_path: str, context: dict) -> str:
    """Render a template with with context to a string."""

    return load(template_path).render(**context)
