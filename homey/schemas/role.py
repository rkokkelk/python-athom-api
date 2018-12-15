from homey.models.role import Role

from marshmallow import Schema, fields, post_load, EXCLUDE

class RoleSchema(Schema):
    _id = fields.String()
    name = fields.String()
    scopes = fields.List(fields.String())

    # Exclude unknown keys
    class Meta:
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Role(**data)
