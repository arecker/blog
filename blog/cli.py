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


if __name__ == '__main__':
    main()