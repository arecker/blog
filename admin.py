import click
import tests


@click.group()
def cli():
    """
    This is the admin script for my blog.
    """
    pass


@cli.command()
@click.option('--silent', is_flag=True, help="Supress output")
def update(silent):
    """
    Refreshes the content cache
    """
    pass


@cli.command()
def test():
    """
    Runs unit tests
    """
    tests.run()


@cli.command()
def email():
    """
    Manages the email subscription engine
    """
    pass


cli.add_command(update)
cli.add_command(test)
cli.add_command(email)
if __name__ == '__main__':
    cli()