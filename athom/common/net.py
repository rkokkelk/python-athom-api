import logging

import requests
from requests.exceptions import ConnectionError, SSLError

from athom.common.exceptions import AthomCloudAuthenticationError, \
                                    AthomCloudGateWayAPIError, \
                                    AthomCloudUnknownAPIError, \
                                    AthomAPIConnectionError

log = logging.getLogger(__name__)

# Timeout for (connect, read)
TIMEOUT = (4, 10)


def post(url, token=None, refresh=True, **kwargs):

    headers = kwargs.get('headers', dict())
    _setup_authorization(token, headers)

    try:
        r = requests.post(
            url=url,
            timeout=TIMEOUT,
            **kwargs
        )

        log.debug("POST [%d]: %s", r.status_code, url)
        return _parse_response(r.status_code, r)

    except (ConnectionError, SSLError) as e:
        log.critical(e)
        raise AthomAPIConnectionError(e)

    except AthomCloudAuthenticationError as e:
        # If authentication error, try to refresh token once
        if not (refresh and token and token.refresh_token): raise e

        token.refresh()

        return post(url, token=token, refresh=False, **kwargs)


def get(url, token=None, refresh=True, **kwargs):

    headers = kwargs.get('headers', dict())
    _setup_authorization(token, headers)

    try:
        r = requests.get(
            url=url,
            timeout=TIMEOUT,
            **kwargs
        )

        log.debug("GET  [%d]: %s", r.status_code, url)
        return _parse_response(r.status_code, r)

    except (ConnectionError, SSLError) as e:
        log.critical(e)
        raise AthomAPIConnectionError(e)

    except AthomCloudAuthenticationError as e:
        # If authentication error, try to refresh token once
        if not (refresh and token and token.refresh_token): raise e

        token.refresh()

        return get(url, token=token, refresh=False, **kwargs)


def _setup_authorization(token, headers):

    if not token:
        return

    headers['authorization'] = "Bearer {}".format(token)


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
