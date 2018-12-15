from athom.models.userdevice import UserDevice

from marshmallow import Schema, fields, post_load, EXCLUDE

class UserDeviceSchema(Schema):
    _id = fields.String()
    name = fields.String()
    platform = fields.String()
    token = fields.String()
    publicKey = fields.String()
    appVersion = fields.String()
    created = fields.DateTime()
    updated = fields.DateTime()
    devMode = fields.Boolean()

    # Exclude unknown keys
    class Meta:
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return UserDevice(**data)
