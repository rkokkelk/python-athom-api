import re
import logging

from http.server import HTTPServer, BaseHTTPRequestHandler

log = logging.getLogger(__name__)

oauth = None

def get_webserver(port=8080):
    address = ('', port)

    # Ignore logging from http server except critical
    logging.getLogger('http').setLevel(logging.CRITICAL)

    httpd = HTTPServer(address, RequestHandler)
    log.info("Starting webserver for catching OAUTH token")

    return httpd


class RequestHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        global oauth

        log.debug("Received GET on webserver")
        log.debug("Path: %s", self.path)
        oauth = re.search(r'(?<=code\=)([\w]{40})', self.path).group(0)

        self.send_response(200)
        self.end_headers()


    def log_message(self, format, *args):
        return
