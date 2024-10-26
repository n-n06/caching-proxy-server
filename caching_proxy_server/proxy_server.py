import requests
import colorama
from http.server import BaseHTTPRequestHandler, HTTPServer

from .cache_handler import CacheHandler

class ProxyServer:
    def __init__(self, port : int = 8080):
        self.port = port
        self.cache = CacheHandler()
    
    def run(self):
        server_address = ('', self.port)
        try: 
            httpd = HTTPServer(server_address, self.RequestHandler)
            colorama.Fore = 'BLUE'
            print(f'Server started on port {self.port}')
            httpd.serve_forever()
        except OSError:
            print()


    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            cache_key = self.path
            cached_response = self.server.cache.get(cache_key)

            print(cached_response)
            
