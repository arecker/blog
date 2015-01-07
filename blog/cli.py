import click
from core import CacheWriter


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
def main_serve():
    """
    serves public cache locally
    """
    import server
    server = server.WebServer()


if __name__ == '__main__':
    main()