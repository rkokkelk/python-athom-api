import sys
import logging

from requests import Request

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
