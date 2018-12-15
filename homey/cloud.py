import logging

from homey.token import Token
from homey.schemas.user import UserSchema
from homey.storage.localstorage import LocalStorage
from homey.common.utils import create_url, get, post
from homey.common.exceptions import AthomCloudAuthenticationError

log = logging.getLogger(__name__)

class AthomCloudAPI:

    def __init__(self, clientId, clientSecret, redirectUrl, autoRefreshTokens=True, storage=None):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.redirectUrl = redirectUrl
        self.autoRefreshTokens = autoRefreshTokens

        self.token = None
        self.storage = LocalStorage() if storage is None else storage

        if 'token' in self.storage:
            token_dict = self.storage.get('token')
            self.token = Token(**token_dict)


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
        self.storage.set('token', self.token.__dict__)

        return self.token


    def getLoginUrl(self):
        params = {
            'client_id': self.clientId,
            'redirect_uri': self.redirectUrl,
            'response_type': 'code'
        }

        return create_url("https://api.athom.com/oauth2/authorise", params)


    def getUser(self):
        url = "https://api.athom.com/user/me"

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = get(url, token=self.token, headers=headers)
            schema = UserSchema()
            user = schema.loads(response)
            return user

        except AthomCloudAuthenticationError as ae:
            if not self.autoRefreshTokens:
                raise ae

            self.refreshTokens()

            return self.getUser()


    def hasAuthorizationCode(self):
        return self.token is not None


    def isLoggedIn(self):
        raise NotImplementedError()


    def refreshTokens(self):
        url = "https://api.athom.com/oauth2/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'grant_type': 'refresh_token',
            'refresh_token': self.token.refresh_token
        }

        r = post(url, data=data, headers=headers)
        self.token = Token.generate_token(r)
        self.storage.set('token', self.token.__dict__)

        return self.token


    def setToken(self, token):
        self.token = token
