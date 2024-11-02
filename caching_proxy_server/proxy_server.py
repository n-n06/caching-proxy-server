import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

from .cache_handler import CacheHandler
from .config import logger

cache = CacheHandler(3600)


class ProxyServer:
    def __init__(self, port : int, origin : str):
        self.port = port
        self.origin = origin
        global ORIGIN
        ORIGIN = origin
        global PORT
        PORT = port
        self.cache = cache

    def run(self):
        server_address = ('', self.port)
        try: 
            httpd = HTTPServer(server_address, self.RequestHandler)
            logger.info('Server started on port http://localhost:%d', self.port)
            httpd.serve_forever()

        except KeyboardInterrupt:
            logger.warning("Server interrupted by user.")
        except requests.exceptions.RequestException as e:
            logger.error("Error forwarding request: %s", e)
        except PermissionError as e:
            logger.error("Permission to the port %d denied", self.port)
        except OSError as e:
            logger.error("Port: %d is already in use or unavailalbe", self.port)
        except Exception as e:
            logger.error("Server encountered an unexpected error: %s", e) #use exc_info=True to get callback
        finally:
            logger.info("Shutting down the proxy server.")
            exit()

    class RequestHandler(BaseHTTPRequestHandler):
        #TODO: change the logic to working with 1 origin and different endpoints     
        

        def do_GET(self):
            cache_key = self.path
            
            try:

                logger.info('Received a GET request for %s', self.path)

                cached_response = cache.get(cache_key)

                if cached_response:
                    logger.info('Cache hit for %s', self.path)
                    self.send_response(200)
                    self.send_header('X-Cache', 'HIT')
                    self.end_headers()
                    self.wfile.write(cached_response)
                    return

                logger.info("Cache miss for %s; fetching from server...", cache_key)
                response = requests.get(f"{ORIGIN}{self.path}")
                response.raise_for_status()

                cache.set(cache_key, response.content)
                self.send_response(response.status_code)
                self.send_header('X-Cache', 'MISS')
                self.end_headers()
                self.wfile.write(response.content)

            except requests.exceptions.RequestException as e:
                self.send_response(502)
                self.end_headers()
                self.wfile.write(b"Error reaching the endpoint")
                logger.error("Request error: %s", e)

            # except KeyError: #related to cache - may delete later
            #     self.send_response(500)
            #     self.end_headers()
            #     self.wfile.write(b"Cache error")
            #
            except BrokenPipeError:
                logger.error("Client disconnected unexpectedly")
            
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Server error")
                logger.error("Unexpected error: %s", e)


