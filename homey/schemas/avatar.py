from homey.models.avatar import Avatar

from marshmallow import Schema, fields, post_load, EXCLUDE

class AvatarSchema(Schema):
    small = fields.URL()
    medium = fields.URL()
    large = fields.URL()

    # Exclude unknown keys
    class Meta:
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Avatar(**data)
