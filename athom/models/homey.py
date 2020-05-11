import logging

from marshmallow import Schema, fields, post_load, EXCLUDE

from athom.homey import HomeyAPI
from athom.common.net import AthomSession

log = logging.getLogger(__name__)


class Homey:

    def __init__(self, _id=None, token=None, **kwargs):
        self._id = _id
        self.name = kwargs.get('name', None)
        self.ipInternal = kwargs.get('ipInternal', None)

        for key, value in kwargs.items():
            setattr(self, key, value)

        # delegationToken is required for homeys/homeyAPI
        self.delegationToken = None
        self.apiVersion = int(self.softwareVersion.split('.')[0])

        # Set request.Session for API interaction
        self.s = AthomSession()

    def __eq__(self, obj):
        return isinstance(obj, Homey) and obj._id == self._id

    def __str__(self):
        return f"{self.name}({self.softwareVersion})"

    def __repr__(self):
        return f"<Homey {self}>"

    def _setDelegationToken(self, token):
        self.delegationToken = token
        self.s = AthomSession(token=token)

    def authenticate(self, token=None, strategy='localSecure'):

        # For Homey v1, auth token is given in json response for getting Homey info
        if self.apiVersion == 1:
            if not self.token and not token:
                message = "A token is required in order to access HomeyAPI for Homey version 1"
                log.error(message)
                raise ValueError(message)

            url = f"http://{self.ipInternal}"
            return HomeyAPI(url, token=self.token)

        # For Homey v2+, auth token is got via delegation
        url = 'https://api.athom.com/delegation/token?audience=homey'

        data = {
            'audience': 'homey'
        }

        self.token = self.s.post(url, json=data).text.replace('"', '')

        if strategy == 'cloud':
            url = self.remoteUrl
        elif strategy == 'localSecure':
            url = self.localUrlSecure
        else:
            url = self.localUrl

        return HomeyAPI(url, token=self.token)


class HomeyUserSchema(Schema):
    user = fields.Nested('UserSchema', exclude=('homeys', ))

    class Meta:
        additional = ['userId', 'role']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return dict(**data)


class GeolocationSchema(Schema):

    class Meta:
        additional = ['latitude', 'longitude', 'accuracy', 'mode']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return dict(**data)


class HomeySchema(Schema):
    #geolocation = fields.Nested(GeolocationSchema)
    users = fields.List(fields.Nested(HomeyUserSchema))

    class Meta:
        additional = ['_id', 'name', 'ipInternal', 'ipExternal', 'softwareVersion',
                      'geolocation', 'language', 'state', 'role', 'token', 'apps',
                      'apiVersion', 'localUrl', 'localUrlSecure', 'remoteUrl']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Homey(**data)
