import logging

import requests
from requests.exceptions import ConnectionError, SSLError

from athom.common.exceptions import AthomCloudAuthenticationError, \
                                    AthomCloudGateWayAPIError, \
                                    AthomCloudUnknownAPIError, \
                                    AthomAPIConnectionError

log = logging.getLogger(__name__)

# Timeout for (connect, read)
TIMEOUT = (4, 30)



def post(url, refresh=True, **kwargs):
    log.debug('POST: %s', url)
    token = kwargs.get('token', None)

    try:
        return _request(
            requests.post,
            url,
            **kwargs
        )

    except AthomCloudAuthenticationError as e:

        # If authentication error, try to refresh token once
        if not isinstance(token, str) and not (refresh and token and token.refresh_token):
            raise e

        token.refresh()

        return post(url, refresh=False, **kwargs)


def delete(url, refresh=True, **kwargs):
    log.debug('DELETE: %s', url)
    token = kwargs.get('token', None)

    try:
        return _request(
            requests.delete,
            url,
            **kwargs
        )

    except AthomCloudAuthenticationError as e:

        # If authentication error, try to refresh token once
        if not isinstance(token, str) and not (refresh and token and token.refresh_token):
            raise e

        token.refresh()

        return delete(url, refresh=False, **kwargs)


def get(url, refresh=True, **kwargs):
    log.debug('GET: %s', url)
    token = kwargs.get('token', None)

    try:
        return _request(
            requests.get,
            url,
            **kwargs
        )

    except AthomCloudAuthenticationError as e:

        # If authentication error, try to refresh token once
        if not isinstance(token, str) and not (refresh and token and token.refresh_token):
            raise e

        token.refresh()

        return get(url, refresh=False, **kwargs)


def put(url, refresh=True, **kwargs):
    token = kwargs.get('token', None)

    try:
        return _request(
            requests.put,
            url,
            **kwargs
        )

    except AthomCloudAuthenticationError as e:

        # If authentication error, try to refresh token once
        if not isinstance(token, str) and not (refresh and token and token.refresh_token):
            raise e

        token.refresh()

        return put(url, refresh=False, **kwargs)




def _request(method, url, token=None, **kwargs):
    headers = kwargs.pop('headers', dict())

    # Verify on None, empty tokens will properly raise error in str(token)
    if token is not None:
        headers['authorization'] = "Bearer {}".format(token)

    try:
        r = method(
            url=url,
            timeout=TIMEOUT,
            headers=headers,
            **kwargs
        )

        return _parse_response(r.status_code, r)

    except (ConnectionError, SSLError) as e:
        error = AthomAPIConnectionError(e)
        log.critical(error)
        raise error


def _parse_response(status_code, response):
    text = response.text

    if status_code == 200:
        return text

    if status_code in (400, 401):
        error = AthomCloudAuthenticationError(text)
        log.warning(error)

    elif status_code == 502:
        error = AthomCloudGateWayAPIError()
        log.warning(error)

    else:
        error = AthomCloudUnknownAPIError(text)
        log.error(error)

    raise error
