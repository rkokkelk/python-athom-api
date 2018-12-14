import logging

from homey.utils import create_url

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

        return create_url("https://api.athom.com/oauth2/authorise", params)

    def setToken(self, token):
        self.token = token
