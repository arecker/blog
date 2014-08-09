import click
from models import Post, ContentItems, Email
import utility
import time
import webbrowser
import requests
import json
import tabulate
import smtplib


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
@click.option('--silent', is_flag=True, help="supress output")
def cli_refresh(silent):
    """
    refresh the content of the public folder
    """

    # Posts
    posts = []
    posts_path = utility.PathGetter.get_posts_directory()

    if silent:
        for file in utility.PathGetter.get_abs_post_file_list():
            post = Post(file)
            utility.write_route(route_name=post.link, data=post, template_name="post.html")
            posts.append(post)
    else:
        with click.progressbar(utility.PathGetter.get_abs_post_file_list(), label="Refreshing posts") as bar:
            for item in bar:
                post = Post(item)
                utility.write_route(route_name=post.link, data=post, template_name="post.html")
                posts.append(post)

    latest_post = posts[-1]

    # Homepage
    if not silent:
        click.echo("Refreshing home")
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
    if not silent:
        click.echo("Refreshing feed.xml")
    latest_post.to_rss()
    utility.write_route(route_name="feed", data=latest_post, template_name="feed.xml", filename="index.xml")

    # Robots.txt
    if not silent:
        click.echo("Refreshing robots.txt")
    utility.write_through_template(template_name="robots.txt", data=None, filename="robots.txt", output_path=utility.PathGetter.get_public_directory())

    # Sitemap
    links = []
    if not silent:
        click.echo("Refreshing sitemap.xml")
    for post in posts:
        links.append('http://alexrecker.com/' + post.link + '/')
    links.append('http://alexrecker.com')
    utility.write_through_template(template_name='sitemap.xml', data=links, filename="sitemap.xml", output_path=utility.PathGetter.get_public_directory())

    # 404
    if not silent:
        click.echo("Refreshing 404.html")
    if not silent:
        click.echo('Done!')
    utility.write_through_template(template_name="404.html", data=None, filename="404.html", output_path=utility.PathGetter.get_public_directory())


@cli.group()
def email():
    """
    manage email subscribers
    """
    pass


@email.command(name="list")
def email_list():
    """
    list email subscribers
    """
    data = get_subscriber_list()
    # Print number
    count = len(data)
    if count is 0:
        print('There are no subscribers.')
        exit()
    elif count is 1:
        print('There is 1 subscriber')
        print("")
    else:
        print('There are ' + str(count) + ' subscribers.')
        print("")

    # Print Table
    table = []
    for sub in data:
        table.append([sub["email"], sub["full_text"], sub["unsubscribe_key"]])
    print tabulate.tabulate(table, headers=["Email", "Full Text", "Key"])


def get_subscriber_list():
    try:
        key = utility.KeyManager.get_admin_key()
        url = "http://api.alexrecker.com/email/subscriber/list/?admin=" + key
        resp = requests.get(url=url)
        data = json.loads(resp.text)
        return data
    except:
        click.echo("Cannot reach API right now")


@email.command(name="delete")
@click.option('--key', prompt="Unsubscribe Key")
def email_delete(key):
    """
    delete a subscriber (key required)
    """
    try:
        url = "http://api.alexrecker.com/email/subscriber/delete?unsubscribe=" + key
        resp = requests.get(url=url)
        click.echo('Subscriber removed')
    except:
        click.echo("Cannot reach API right now")


@email.command(name="send")
@click.option('--test', is_flag=True, help="writes out email to html files")
def email_send(test=False):
    """
    send the blog post to subscribers
    """
    try:
        my_email = utility.KeyManager.get_email()
        email_password = utility.KeyManager.get_email_password()
    except:
        my_email = click.prompt('Email')
        email_password = click.prompt('Password')

    # Get Data
    post = Post(utility.PathGetter.get_abs_post_file_list()[-1])
    subscribers = get_subscriber_list()

    print('You are about to send out ' + str(len(subscribers)) + ' emails.')
    print('Post: ' + post.title)
    if not click.confirm('Church?'):
        print('Whatever')
        exit()

    # Open Email Session
    if not test:
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.ehlo()
        session.starttls()
        session.login(my_email, email_password)

    with click.progressbar(subscribers,label="Sending...") as bar:
        for person in bar:
            email = Email(
                sender = "Alex Recker",
                recipient = person["email"],
                subject = post.title,
                post = post,
                unsubscribe_key = person["unsubscribe_key"],
                full_text = person["full_text"]
            )

            headers = "\r\n".join(["from: " + email.sender,
                           "subject: " + email.subject,
                           "to: " + email.recipient,
                           "mime-version: 1.0",
                           "content-type: text/html"])

            body = utility.get_html_from_template(template_name="email.html", data=email)
            content = headers + "\r\n\r\n" + body

            if not test:
                session.sendmail(my_email, email.recipient, content)
                session.close()
            else:
                utility.write_through_template(output_path='.', template_name="email.html", data=email, filename=email.recipient + '.html')


if __name__ == '__main__':
    cli()
