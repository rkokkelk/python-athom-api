import logging

from marshmallow import Schema, fields, post_load, EXCLUDE

from athom.homey import HomeyAPI

log = logging.getLogger(__name__)

class Homey:

    def __init__(self, _id=None, token=None, **kwargs):
        self._id = _id
        self.token = token
        self.name = kwargs.get('name', None)
        self.ipInternal = kwargs.get('ipInternal', None)

        for key, value in kwargs.items():
            setattr(self, key, value)


    def __str__(self):
        return "[{self._id}] {self.name} ({self.softwareVersion})".format(self=self)


    def authenticate(self, token=None, strategy=None):

        if strategy and strategy != "cloud":
            message = "This module can only be used in cloud modus"
            log.error(message)
            raise ValueError(message)

        if not token and not self.token:
            message = "A token is required in order to access HomeyAPI"
            log.error(message)
            raise ValueError(message)

        return HomeyAPI(self.ipInternal, token=self.token)


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
                      'geolocation', 'language', 'state', 'role', 'token', 'apps']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Homey(**data)
