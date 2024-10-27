import click

from .config import logger
from .proxy_server import ProxyServer


@click.command()
@click.option("--port", "-p", required=True, type=int, help="Proxy server port")
@click.option("--origin", "-o", required=True, type=str, help="URL of the target server")
@click.option("--clear-cache", is_flag=True, help="Clear the proxy server's cache")
def cli(port: int, origin: str, clear_cache):
    proxy = ProxyServer(port)
    if clear_cache:
        



if __name__ == '__main__':
    cli()
