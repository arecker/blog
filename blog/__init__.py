import jinja2
import os

HERE = os.path.join(os.path.dirname(os.path.realpath(__file__)))


def main():
    env = jinja2.Environment(loader=jinja2.BaseLoader)

    with open(os.path.join(HERE, 'template.html.j2')) as f:
        template = env.from_string(f.read())

    data = template.render()
    print(data)
