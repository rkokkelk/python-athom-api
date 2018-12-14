import sys
import logging
import requests

log = logging.getLogger(__name__)

def post(url, data):
    r = requests.post(
        url=url,
        data=data
    )

    if not r.response_code:
        raise Exception()

    return r.text

def setup_logging(debug=False):

    default_formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d [%(levelname)-.1s]: %(message)s",
        "%H:%M:%S"
    )

    r_log = logging.getLogger('homey')

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(default_formatter)

    if debug:
        r_log.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)

    r_log.addHandler(ch)

