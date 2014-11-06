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


if __name__ == '__main__':
    cli()