import logging
import requests

from athom.common.exceptions import AthomCloudAuthenticationError, \
                                    AthomCloudGateWayAPIError, \
                                    AthomCloudUnknownAPIError

log = logging.getLogger(__name__)


def post(url, token=None, refresh=True, **kwargs):

    if token:
        kwargs['headers'] = _setup_authorization(token, kwargs['headers'])

    try:
        r = requests.post(
            url=url,
            **kwargs,
        )

        log.debug("POST [%d]: %s", r.status_code, url)
        return _parse_response(r.status_code, r)
 
    except AthomCloudAuthenticationError as e:
        # If authentication error, try to refresh token once
        if not (refresh and token and token.refresh_token): raise e

        token.refresh()

        return post(url, token=token, refresh=False, **kwargs)


def get(url, token=None, refresh=True, **kwargs):

    if token:
        kwargs['headers'] = _setup_authorization(token, kwargs['headers'])

    try:
        r = requests.get(
            url=url,
            **kwargs
        )

        log.debug("GET  [%d]: %s", r.status_code, url)
        return _parse_response(r.status_code, r)
    
    except AthomCloudAuthenticationError as e:
        # If authentication error, try to refresh token once
        if not (refresh and token and token.refresh_token): raise e

        token.refresh()

        return get(url, token=token, refresh=False, **kwargs)


def _setup_authorization(token, headers):

    if not headers:
        headers = dict()

    headers['authorization'] = "Bearer {}".format(token)

    return headers


def _parse_response(status_code, response):
    text = response.text

    if status_code == 200:
        return text

    if status_code == 401:
        error = AthomCloudAuthenticationError(text)
        log.warning(error)

    elif status_code == 502:
        error = AthomCloudGateWayAPIError()
        log.warning(error)

    else:
        error = AthomCloudUnknownAPIError(text)
        log.error(error)

    raise error
