import logging

from athom.token import Token
from athom.models.user import UserSchema
from athom.storage.localstorage import LocalStorage
from athom.common.net import AthomSession
from athom.common.utils import create_url
from athom.common.exceptions import AthomAPISessionError

log = logging.getLogger(__name__)


class AthomCloudAPI:

    def __init__(self, clientId, clientSecret, redirectUrl, **kwargs):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.redirectUrl = redirectUrl

        self.storage = kwargs.get('storage', LocalStorage())
        self.autoRefreshTokens = kwargs.get('autoRefreshTokens', True)

        if 'token' in self.storage:
            token_dict = self.storage.get('token')
            self.token = Token(self, **token_dict)
        else:
            self.token = kwargs.get('token', Token(self))

        # Set request.Session for API interaction
        self.s = AthomSession(base='https://api.athom.com', token=self.token)

    def authenticateWithAuthorizationCode(self, oauth):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'grant_type': 'authorization_code',
            'code': oauth
        }

        r = self.s.post('/oauth2/token', data=data, headers=headers)

        self.token = Token.generate_token(self, r.json())
        self.storage.set('token', self.token.jsonify())

        return self.token

    def getLoginUrl(self, scopes=[]):
        params = {
            'client_id': self.clientId,
            'redirect_uri': self.redirectUrl,
            'response_type': 'code',
            'scopes': ','.join(scopes)
        }

        return create_url('https://api.athom.com/oauth2/authorise', params)

    def getUser(self):
        response = self.s.get('/user/me')
        schema = UserSchema()
        user = schema.loads(response.text)

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
