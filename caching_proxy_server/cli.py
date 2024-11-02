import click

from .config import logger
from .proxy_server import ProxyServer




@click.command()
@click.option("--port", "-p", type=int, help="Proxy server port")
@click.option("--origin", "-o", type=str, help="URL of the target server")
@click.option("--clear-cache", is_flag=True, help="Clear the proxy server's cache")
def cli(port: int, origin: str, clear_cache):
    '''
    Minimalist caching proxy server. 
    '''
    proxy = ProxyServer(port, origin)
    if clear_cache:
        proxy.cache.clear()
    elif port is not None and origin is not None: 
        try:
            proxy.run()
        except KeyboardInterrupt:
            proxy.stop()
    else:
        logger.error('Please provide either both --port and --origin or use --clear-cache')



if __name__ == '__main__':
    cli()
