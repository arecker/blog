import jinja2
import os


def write_through_template(output_path, template_name, data, filename, templates_path=None):
    if not templates_path:
        templates_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
    j_template = env.get_template(template_name)
    with open(os.path.join(output_path, filename), 'wb') as file:
        file.write(j_template.render(data = data))