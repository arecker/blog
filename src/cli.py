import click
from models import Post, ContentItems
import utility
import time
import webbrowser


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
    path = post.link + '.html'
    webbrowser.open(url=path, autoraise=True)


@cli.command(name="refresh")
def cli_refresh():
    """
    refresh the content of the public folder
    """

    # Posts
    posts = []
    posts_path = utility.PathGetter.get_posts_directory()
    for file in utility.PathGetter.get_abs_post_file_list():
        post = Post(file)
        utility.write_route(route_name=post.link, data=post, template_name="post.html")
        posts.append(post)
    latest_post = posts[-1]

    # Homepage
    content_path = utility.PathGetter.get_content_path()
    ci = ContentItems(content_path)

    home_data = {
        "latest": {
            "title": latest_post.title,
            "image": latest_post.image,
            "description": latest_post.description,
            "link": latest_post.link
        },

        "posts": reversed(posts),
        "friends": ci.friends,
        "projects": ci.projects
    }

    public_dir = utility.PathGetter.get_public_directory()
    utility.write_through_template(output_path=public_dir, template_name="home.html", data=home_data, filename="index.html")

    # RSS
    #latest_post.to_rss()
    #utility.write_route(route_name="feed", data=latest_post, tempalte_name="feed.xml")



if __name__ == '__main__':
    cli()