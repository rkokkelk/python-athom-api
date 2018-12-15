from athom.models.user import User
from athom.schemas.role import RoleSchema
from athom.schemas.homey import HomeySchema
from athom.schemas.avatar import AvatarSchema
from athom.schemas.userdevice import UserDeviceSchema

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
