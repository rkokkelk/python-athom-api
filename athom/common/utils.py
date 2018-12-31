import sys
import logging

import requests
from requests import Request

from athom.token import Token
from athom.common.exceptions import AthomCloudAuthenticationError, \
                                    AthomCloudGateWayAPIError, \
                                    AthomCloudUnknownAPIError

log = logging.getLogger(__name__)


def json(url, data, token=None, headers=dict()):

    setup_authorization(token, headers)

    r = requests.post(
        url=url,
        json=data,
        headers=headers
    )

    log.debug("POST/JSON [%d]: %s", r.status_code, url)
    print(r.request.headers)
    print(r.request.body)

    if r.status_code == 200:
        return r.text

    if r.status_code == 401:
        error = AthomCloudAuthenticationError(r.text)

    if r.status_code == 502:
        error = AthomCloudGateWayAPIError()

    else:
        error = AthomCloudUnknownAPIError(r.text)

    log.error(error)
    raise error


def post(url, data, token=None, headers=dict()):

    setup_authorization(token, headers)

    r = requests.post(
        url=url,
        data=data,
        headers=headers
    )

    log.debug("POST [%d]: %s", r.status_code, url)

    if r.status_code == 200:
        return r.text

    if r.status_code == 401:
        error = AthomCloudAuthenticationError(r.text)

    if r.status_code == 502:
        error = AthomCloudGateWayAPIError()

    else:
        error = AthomCloudUnknownAPIError(r.text)

    log.error(error)
    raise error


def get(url, params=None, token=None, headers=dict()):

    setup_authorization(token, headers)

    r = requests.get(
        url=url,
        params=params,
        headers=headers
    )

    log.debug("GET  [%d]: %s", r.status_code, url)

    if r.status_code == 200:
        return r.text

    if r.status_code == 401:
        error = AthomCloudAuthenticationError(r.text)

    if r.status_code == 502:
        error = AthomCloudGateWayAPIError()

    else:
        error = AthomCloudUnknownAPIError(r.text)

    log.error(error)
    raise error


def setup_authorization(token, headers):
    if not token:
        return

    if type(token) is Token:
        headers['authorization'] = "Bearer {}".format(token.access_token)
    else:
        headers['authorization'] = "Bearer {}".format(token)


def create_url(url, params):
    p = Request('GET', url, params=params).prepare()
    return p.url


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
