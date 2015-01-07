import click
from core import CacheWriter, Config


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
def main_serve(r):
    """
    serves public cache locally
    """
    import server
    if r:
        CacheWriter.refresh_public()
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


if __name__ == '__main__':
    main()