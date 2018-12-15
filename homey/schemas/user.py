from homey.models.user import User

from marshmallow import Schema, fields, post_load, EXCLUDE

class UserSchema(Schema):
    _id = fields.String()
    firstname = fields.String()
    lastname = fields.String()
    email = fields.Email()
    language = fields.String()
    roleIds = fields.List(fields.String())

    # Exclude unknown keys
    class Meta:
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        print(data)
        return User(**data)
