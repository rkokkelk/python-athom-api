from marshmallow import Schema, fields, post_load, EXCLUDE

class Avatar:

    def __init__(self, small=None, medium=None, large=None):
        self.small = small
        self.medium = medium
        self.large = large


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
