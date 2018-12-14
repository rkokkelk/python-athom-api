import logging

from requests import Request

log = logging.getLogger(__name__)

class AthomCloudAPI:

    clientId = None
    clientSecret = None
    redirectUrl = None
    token = None

    def __init__(self, clientId, clientSecret, redirectUrl):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.redirectUrl = redirectUrl

        log.debug("Constructor AthomCloudAPI")

    def getLoginUrl(self):
        params = {
            'client_id': self.clientId,
            'redirect_uri': self.redirectUrl,
            'response_type': 'code'
        }

        p = Request('GET', 'https://api.athom.com/oauth2/authorise',
                    params=params
                   ).prepare()

        return p.url

    def setToken(self, token):
        self.token = token
