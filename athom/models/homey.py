import logging

from marshmallow import Schema, fields, post_load, EXCLUDE

from athom.homey import HomeyAPI
from athom.common.net import get, post

log = logging.getLogger(__name__)

class Homey:

    def __init__(self, _id=None, token=None, **kwargs):
        self._id = _id
        self.token = token
        self.name = kwargs.get('name', None)
        self.ipInternal = kwargs.get('ipInternal', None)

        for key, value in kwargs.items():
            setattr(self, key, value)

        # delegationToken is required for homeys/homeyAPI
        self.delegationToken = None
        #self.apiVersion = int(self.softwareVersion.split('.')[0])

    def __str__(self):
        return "[{self._id}] {self.name} ({self.softwareVersion})".format(self=self)


    def authenticate(self, token=None, strategy='localSecure'):

        # For Homey v1, auth token is given in json response for getting Homey info
        if self.apiVersion == 1:
            if not self.token and not token:
                message = "A token is required in order to access HomeyAPI for Homey version 1"
                log.error(message)
                raise ValueError(message)

            url = "http://{self.ipInternal}".format(self=self)
            return HomeyAPI(url, token=self.token)

        # For Homey v2+, auth token is got via delegation
        url = 'https://api.athom.com/delegation/token?audience=homey'

        data = {
            'audience': 'homey'
        }

        self.token = post(url, json=data, token=self.delegationToken).replace('"', '')

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
