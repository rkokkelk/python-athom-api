from homey.models.user import User
from homey.schemas.role import RoleSchema
from homey.schemas.homey import HomeySchema
from homey.schemas.avatar import AvatarSchema
from homey.schemas.userdevice import UserDeviceSchema

from marshmallow import Schema, fields, post_load, EXCLUDE

class UserSchema(Schema):
    _id = fields.String()
    firstname = fields.String()
    lastname = fields.String()
    email = fields.Email()
    language = fields.String()
    roles = fields.List(fields.Nested(RoleSchema))
    roleIds = fields.List(fields.String())
    avatar = fields.Nested(AvatarSchema)
    homeys = fields.List(fields.Nested(HomeySchema))
    devices = fields.List(fields.Nested(UserDeviceSchema))

    # Exclude unknown keys
    class Meta:
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return User(**data)
