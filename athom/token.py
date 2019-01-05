import json
import logging

from athom.common.net import get, post

log = logging.getLogger(__name__)

class Token:

    def __init__(self, athom, **kwargs):
        self.access_token = kwargs.get('access_token', None)
        self.expires_in = kwargs.get('expires_in', -1)
        self.token_type = kwargs.get('token_type', 'bearer')
        self.refresh_token = kwargs.get('refresh_token', None)

        self.athom = athom


    def jsonify(self):
        columns = ['access_token', 'expires_in', 'token_type', 'refresh_token']
        return {k:v for k, v in self.__dict__.items() if k in columns}


    def refresh(self):
        url = "https://api.athom.com/oauth2/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'client_id': self.athom.clientId,
            'client_secret': self.athom.clientSecret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        log.info("Refreshing token")
        r = post(url, data=data, headers=headers)

        data = json.loads(r)
        for key, value in data.items():
            setattr(self, key, value)

        self.athom.storage.set('token', self.jsonify())


    def __str__(self):
        """ Standard string representation. Access_token defines Token object
        """
        return self.access_token


    @staticmethod
    def generate_token(athom, json_str):
        token = Token(athom)
        data = json.loads(json_str)

        for key, value in data.items():
            setattr(token, key, value)

        return token
