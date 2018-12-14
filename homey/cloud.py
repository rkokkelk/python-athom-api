import logging

from homey.token import Token
from homey.utils import create_url, get, post

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


    def authenticateWithAuthorizationCode(self, oauth):
        url = "https://api.athom.com/oauth2/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'grant_type': 'authorization_code',
            'code': oauth
        }

        r = post(url, data=data, headers=headers)
        self.token = Token.generate_token(r)


    def getUser(self):
        url = "https://api.athom.com/user/me"

        headers = {
            'Content-Type': 'application/json'
        }

        me = get(url, token=self.token, headers=headers)
        log.debug(me)


    def setToken(self, token):
        self.token = token
