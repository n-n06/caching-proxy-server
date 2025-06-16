from threading import Thread
from typing import Any

import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

from .cache_handler import CacheHandler
from .config import logger

cache = CacheHandler(3600)


class ProxyServer:
    def __init__(self, port: int, origin: str):
        self.port = port
        self.origin = origin
        global ORIGIN
        ORIGIN = origin
        global PORT
        PORT = port
        self.cache = cache

        self.httpd: HTTPServer
        self.server_thread: Thread

    def run(self):
        server_address = ("", self.port)
        self.httpd = HTTPServer(server_address, self.RequestHandler)

        def start_server():
            try:
                logger.info("Server started on port http://localhost:%d.", self.port)
                self.httpd.serve_forever()
            except requests.exceptions.RequestException as e:
                logger.error("Error forwarding request: %s.", e)
            except PermissionError:
                logger.error("Permission to the port %d denied.", self.port)
            except OSError:
                logger.error("Port: %d is already in use or unavailalbe.", self.port)
            except Exception as e:
                logger.error(
                    "Server encountered an unexpected error: %s.", e
                )  # use exc_info=True to get callback
            finally:
                logger.info("Proxy server has been successfully stopped.")

        self.server_thread = Thread(target=start_server)
        self.server_thread.start()

    def stop(self):
        if self.httpd:
            self.cache.save_cache()
            self.httpd.shutdown()
            self.httpd.server_close()
            self.server_thread.join()
            logger.info("Shutting down the proxy server.")

    class RequestHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:
            """
            Suppressing the default logger
            """
            pass

        def handle_proxy_request(self):
            method = self.command
            url = f"{ORIGIN}{self.path}"
            headers = {
                k: v for k, v in self.headers.items()
                if k.lower() != "host" # ignore the host headers
            }
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(
                content_length
            ) if content_length > 0 else None

            try:
                logger.info("Received a %s request for %s", method, self.path)

                if method == "GET":
                    # Retrieve only GET requests from cache
                    cached_response = cache.get(self.path)

                    if cached_response:
                        logger.info("Cache hit for %s", self.path)
                        self.send_response(200)
                        self.send_header("X-Cache", "HIT")
                        self.end_headers()
                        self.wfile.write(cached_response)
                        return
        
                    logger.info("Cache miss for %s", self.path)

                # Execute the actual response
                response = requests.request(
                    method, url, headers=headers, data=body
                )
                response.raise_for_status()

                if method == "GET":
                    # Cache only get requests
                    cache.set(self.path, response.content)

                self.send_response(response.status_code)

                # Ignoring headers to avoid confusion
                ignored_headers = (
                    'transfer-encoding',
                    'content-length',
                    'content-encoding'
                )
                for key, value in response.headers.items():
                    if key.lower() not in ignored_headers:
                        self.send_header(key, value)

                if method == "GET":
                    self.send_header("X-Cache", "MISS")
                
                self.end_headers()
                self.wfile.write(response.content)

            except requests.exceptions.RequestException as e:
                logger.error("Request error: %s", e)
                self.send_response(502)
                self.end_headers()
                self.wfile.write(b"Bad gateway")

            except BrokenPipeError:
                logger.error("Client disconnected unexpectedly")

            except Exception as e:
                logger.error("Unexpected error: %s", e)
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Server error")

        # Handle all Request types
        def do_GET(self):
            self.handle_proxy_request()

        def do_POST(self):
            self.handle_proxy_request()

        def do_PUT(self):
            self.handle_proxy_request()

        def do_DELETE(self):
            self.handle_proxy_request()

        def do_PATCH(self):
            self.handle_proxy_request()

        def do_HEAD(self):
            self.handle_proxy_request()

        def do_OPTIONS(self):
            self.handle_proxy_request()
