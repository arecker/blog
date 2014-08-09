import click
from models import Post, ContentItems
import utility
import time
import webbrowser
import os


@click.group()
def cli():
    """
    This is the script for my blog.
    It does things.
    """
    pass


@cli.command(name="preview")
@click.argument('file', type=click.Path(exists=True))
def cli_preview(file):
    """
    preview a post in html
    """
    click.echo("Creating post...")
    date = time.strftime("%Y-%d-%m")
    post = Post(file, date_override=date)
    utility.write_through_template(output_path=".", template_name="post.html", data=post, filename=post.link + '.html')
    click.echo("Opening...")
    path = os.path.join('.', post.link + '.html')
    webbrowser.open(url=path, autoraise=True)


if __name__ == '__main__':
    cli()