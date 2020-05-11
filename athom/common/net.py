import logging

from requests import Session
from requests.exceptions import ConnectionError, SSLError

from athom.common.exceptions import AthomCloudAuthenticationError, \
                                    AthomCloudGateWayAPIError, \
                                    AthomCloudUnknownAPIError, \
                                    AthomAPIConnectionError

log = logging.getLogger(__name__)


class AthomSession(Session):

    def __init__(self, **kwargs):
        self.token = kwargs.pop('token', None)
        self.base = kwargs.pop('base', '')

        super().__init__(**kwargs)

    def prepare_request(self, request):
        request.url = self.base + request.url
        request.timeout = (4, 30)  # Timeout for (connect, read)

        if self.token:
            request.headers['authorization'] = f"Bearer {self.token}"

        return super().prepare_request(request)

    def request(self, method, url, **kwargs):
        log.debug('%s: %s', method, url)
        refresh = kwargs.pop('refresh', True)

        try:
            r = super().request(method, url, **kwargs)
            return self._parse_response(r.status_code, r)

        except (ConnectionError, SSLError) as e:
            error = AthomAPIConnectionError(e)
            log.critical(error)
            raise error

        except AthomCloudAuthenticationError as e:

            # If authentication error, try to refresh token once
            if not (refresh and self.token and self.token.refresh_token):
                raise e

            self.token.refresh()

            r = super().request(method, url, **kwargs)
            return self._parse_response(r.status_code, r)

    def _parse_response(self, status_code, response):
        text = response.text

        if status_code in range(200, 299):
            return response

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
