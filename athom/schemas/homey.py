from athom.models.homey import Homey

from marshmallow import Schema, fields, post_load, EXCLUDE

class HomeyUserSchema(Schema):
    user = fields.Nested('UserSchema', exclude=('homeys', ))
    userId = fields.String()
    role = fields.String()

    @post_load
    def create_obj(self, data):
        return dict(**data)


class GeolocationSchema(Schema):
    latitude = fields.Float()
    longitude = fields.Float()
    accuracy = fields.Integer()
    mode = fields.String()

    @post_load
    def create_obj(self, data):
        return dict(**data)


class HomeySchema(Schema):
    _id = fields.String()
    name = fields.String()
    ipInternal = fields.String()
    ipExternal = fields.String()
    softwareVersion = fields.String()
    language = fields.String()
    state = fields.String()
    geolocation = fields.Nested(GeolocationSchema)
    users = fields.List(fields.Nested(HomeyUserSchema))
    role = fields.String()
    token = fields.String()
    apps = fields.List(fields.Dict(values=fields.String(), keys=fields.String()))

    # Exclude unknown keys
    class Meta:
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Homey(**data)
