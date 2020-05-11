import logging

from athom.models.role import RoleSchema
from athom.models.homey import HomeySchema
from athom.models.avatar import AvatarSchema
from athom.models.userdevice import UserDeviceSchema

from marshmallow import Schema, fields, post_load, EXCLUDE

log = logging.getLogger(__name__)


class User:

    def __init__(self, _id=None, **kwargs):
        self._id = _id
        self.firstname = kwargs.pop('firstname', None)
        self.lastname = kwargs.pop('lastname', None)
        self.devices = kwargs.pop('devices', list())
        self.homeys = kwargs.pop('homeys', list())

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, obj):
        return isinstance(obj, User) and obj._id == self._id

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def __repr__(self):
        return f"<User {self}>"

    def getDevice(self, d_id):

        for device in self.devices:
            if device._id == d_id:
                return device

        raise LookupError()

    def getHomeys(self):
        return self.homeys

    def getHomeyById(self, h_id):

        for homey in self.homeys:
            if homey._id == h_id:
                return homey

        raise LookupError()

    def getFirstHomey(self):

        if self.homeys:
            return self.homeys[0]

        raise LookupError()

    def _setDelegationToken(self, token):
        """
        OAUTH token is required by all homey objects, in order to use
        to get delegation token for access to homeyAPI
        """
        for homey in self.homeys:
            homey._setDelegationToken(token)


class UserSchema(Schema):
    avatar = fields.Nested(AvatarSchema)
    roles = fields.List(fields.Nested(RoleSchema))
    homeys = fields.List(fields.Nested(HomeySchema))
    devices = fields.List(fields.Nested(UserDeviceSchema))

    class Meta:
        additional = ['_id', 'firstname', 'lastname', 'email', 'language', 'roleIds']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return User(**data)
