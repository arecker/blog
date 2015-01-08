import click
from core import CacheWriter, Config, Email, Post, Data


@click.group()
def main():
    """
    blog - the CLI edition
    """
    pass


@main.command(name="refresh")
def main_refresh():
    """
    regenerates the site from source files
    """
    CacheWriter.refresh_public()


@main.command(name="serve")
@click.option('-r', is_flag=True, help='refresh site before serving')
@click.option('-b', is_flag=True, help='open in default web browser')
def main_serve(r, b):
    """
    serves public cache locally
    """
    import server
    import threading
    import webbrowser
    if r:
        CacheWriter.refresh_public()

    if b:
        url = "http://127.0.0.1:5000"
        threading.Timer(1.25, lambda: webbrowser.open(url) ).start()
    server = server.WebServer()


@main.command(name="deploy")
@click.option('-r', is_flag=True, help='refresh site before deploying')
def main_deploy(r):
    """
    deploys public folder to server
    """
    if r:
        CacheWriter.refresh_public()
    c = Config()
    if not click.confirm('Deploy public folder to ' + c.deploy_host + ':' + c.deploy_path + '?'):
        exit()


@main.group(name="mail")
def main_mail():
    """
    manage email subscription
    """
    pass


@main_mail.command(name="list")
def mail_list():
    """
    list current subscribers
    """
    import tabulate
    data = Email.get_subscriber_list(Config().api_key)
    count = len(data)
    if count is 0:
        print('There are no subscribers.')
        exit()
    elif count is 1:
        print('There is 1 subscriber\n')
    else:
        print('There are ' + str(count) + ' subscribers.\n')
    table = []
    for sub in data:
        table.append([sub["email"], sub["full_text"], sub["unsubscribe_key"]])
    print(tabulate.tabulate(table, headers=["Email", "Full Text", "Key"]))


@main_mail.command(name="latest")
@click.option('--test', is_flag=True, help="writes emails locally instead of sending them")
def mail_latest(test):
    """
    send latest post to subscribers
    """
    latest = Post.get_all_posts()[0]
    emails = []
    with click.progressbar(Email.get_subscriber_list(Config().api_key), label=" building emails") as bar:
        for sub in bar:
            data = Data()
            data.email = sub["email"]
            data.unsubscribe_key = sub["unsubscribe_key"]
            data.full_text = sub["full_text"]
            data.post = latest
            emails.append(Email(data))
    print('You are about to send out ' + str(len(emails)) + ' emails.')
    print('Post: ' + latest.title)
    if test:
        print('(just testing)')
    if not click.confirm('Church?'):
        print('Whatever')
        exit()
    click.echo(click.style('+ Let\'r rip', fg='green'))
    if test:
        progress_bar_label = "Sending messages (test)"
    else:
        progress_bar_label = "Sending messages"
    with click.progressbar(emails, label=progress_bar_label) as bar:
        for email in bar:
            email.send(test=test)


if __name__ == '__main__':
    main()