import sys
import logging

import requests
from requests import Request

from athom.token import Token
from athom.common.exceptions import AthomCloudAuthenticationError, \
                                    AthomCloudGateWayAPIError, \
                                    AthomCloudUnknownAPIError

log = logging.getLogger(__name__)


def post(url, data=None, json=None, token=None, headers=dict()):

    setup_authorization(token, headers)

    if data:
        r = requests.post(
            url=url,
            data=data,
            headers=headers
        )

    else:
        r = requests.post(
            url=url,
            json=json,
            headers=headers
        )

    log.debug("POST [%d]: %s", r.status_code, url)

    return _parse_response(r.status_code, r)


def get(url, params=None, token=None, headers=dict()):

    setup_authorization(token, headers)

    r = requests.get(
        url=url,
        params=params,
        headers=headers
    )

    log.debug("GET  [%d]: %s", r.status_code, url)
    return _parse_response(r.status_code, r)


def setup_authorization(token, headers):
    if not token:
        return

    if type(token) is Token:
        headers['authorization'] = "Bearer {}".format(token.access_token)
    else:
        headers['authorization'] = "Bearer {}".format(token)


def _parse_response(status_code, response):
    text = response.text

    if status_code == 200:
        return text

    if status_code == 401:
        error = AthomCloudAuthenticationError(text)

    elif status_code == 502:
        error = AthomCloudGateWayAPIError()

    else:
        error = AthomCloudUnknownAPIError(text)

    log.error(error)
    raise error
