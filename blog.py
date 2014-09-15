import click
import jinja2
import os


@click.group()
def cli():
    """
    This is the script for my blog.
    It does things.
    """
    pass


class Utility:
	"""
	File IO, getting paths, and general crap work
	"""

	# Paths
	ROOT = os.path.dirname(os.path.realpath(__file__))
	TEMPLATES = os.path.join(ROOT, 'templates')
	POSTS = os.path.join(ROOT, 'posts')
	PUBLIC = os.path.join(ROOT, 'public')
	DOCS = os.path.join(ROOT, 'docs')
	if not os.path.exists(PUBLIC):
		os.mkdir(PUBLIC)


	@staticmethod
	def render_html_from_template(template, data):
		"""
		takes a template name and data
		returns an html string
		"""
		env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES))
		if test:
			env = jinja2.Environment(loader=jinja2.FileSystemLoader(DOCS))
		j_template = env.get_template(template)
		return j_template.render(data = data)


	@staticmethod
	def write_page(template, data, name, path=PUBLIC, test=False):
		"""
		takes a template name, page data, and a page name
		writes the page name to the path
		"""
		output = render_html_from_template(template=template, data=data, test=test)
		with open(os.path.join(path, name), 'wb') as file:
			file.write(output)


	@staticmethod
	def write_route(template, data, route, root=PUBLIC, test=False):
		"""
		creates a folder in public
		and writes data into an index.html within that folder
		"""
		path = os.path.join(root, route)
		os.makedirs(path)
		write_page(template=template, data=data, name="index.html", path=path, test=test)
