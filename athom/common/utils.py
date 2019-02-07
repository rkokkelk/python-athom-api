import sys
import logging

from requests import Request
from urllib.parse import urlparse

log = logging.getLogger(__name__)


def create_url(url, params):
    p = Request('GET', url, params=params).prepare()
    return p.url


def setup_logging(debug=False):

    default_formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d [%(levelname)-.1s]: %(message)s",
        "%H:%M:%S"
    )

    r_log = logging.getLogger('athom')

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(default_formatter)

    if debug:
        r_log.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)

    r_log.addHandler(ch)


def parse_callback(callback_url):
    url = urlparse(callback_url)

    if not url.port:
        if 'https' in url.scheme:
            return (url.hostname, 443)

        return (url.hostname, 80)

    return (url.hostname, url.port)
