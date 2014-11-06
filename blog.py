import click


@click.group()
def cli():
    pass


@cli.command(name="refresh")
def cli_refresh():
    """
    regenerate the site html cache
    """
    pass


@cli.command(name="serve")
def cli_serve():
    """
    serve site locally
    """
    pass


@cli.command(name="deploy")
def cli_deploy():
    """
    sync server's html cache with project's
    """
    pass


@cli.group(name="mail")
def cli_mail():
    """
    manage email subscription engine
    """
    pass


@cli_mail.command(name="list")
def cli_mail_list():
    """
    list current subscribers
    """
    pass


@cli_mail.command(name="add")
def cli_mail_add():
    """
    add a subscriber
    """
    pass


@cli_mail.command(name="remove")
def cli_mail_remove():
    """
    remove a subscriber
    """
    pass


@cli_mail.command(name="latest")
def cli_mail_latest():
    """
    send latest post to subscribers
    """
    pass


if __name__ == '__main__':
    cli()
