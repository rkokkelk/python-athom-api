import logging

from athom.token import Token
from athom.models.user import UserSchema
from athom.storage.localstorage import LocalStorage
from athom.common.net import get, post
from athom.common.utils import create_url
from athom.common.exceptions import AthomAPISessionError

log = logging.getLogger(__name__)

class AthomCloudAPI:

    def __init__(self, clientId, clientSecret, redirectUrl, **kwargs):
        self.basePath = 'https://api.athom.com'

        self.clientId = clientId
        self.clientSecret = clientSecret
        self.redirectUrl = redirectUrl

        self.token = kwargs.get('token', Token(self))
        self.storage = kwargs.get('storage', LocalStorage())
        self.autoRefreshTokens = kwargs.get('autoRefreshTokens', True)

        if 'token' in self.storage:
            token_dict = self.storage.get('token')
            self.token = Token(self, **token_dict)


    def authenticateWithAuthorizationCode(self, oauth):
        url = self.basePath+"/oauth2/token"

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

        self.token = Token.generate_token(self, r)
        self.storage.set('token', self.token.jsonify())

        return self.token


    def getLoginUrl(self, scopes=[]):
        url = self.basePath+"/oauth2/authorise"

        params = {
            'client_id': self.clientId,
            'redirect_uri': self.redirectUrl,
            'response_type': 'code',
            'scopes': ','.join(scopes)
        }

        return create_url(url, params)


    def getUser(self):
        url = self.basePath+"/user/me"

        headers = {
            'Content-Type': 'application/json'
        }

        response = get(url, token=self.token, headers=headers)
        schema = UserSchema()
        user = schema.loads(response)

        # delegationToken is required for homeys/homeyAPI
        user._setDelegationToken(self.token)
        return user


    def hasAuthorizationCode(self):
        return self.token is not None and self.token


    def isLoggedIn(self):
        try:
            return self.getUser() is not None
        except AthomAPISessionError:
            return False


    def refreshTokens(self, **kwargs):
        token = kwargs.get('token', self.token)
        token.refresh()
        return token


    def enableAutoRefreshTokens(self):
        self.autoRefreshTokens = True


    def disableAutoRefreshTokens(self):
        self.autoRefreshTokens = False


    def setToken(self, token):
        self.token = token


    def setConfig(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
