from marshmallow import Schema, fields, post_load, EXCLUDE


class Avatar:

    def __init__(self, small=None, medium=None, large=None):
        self.small = small
        self.medium = medium
        self.large = large

    def __eq__(self, obj):
        if not isinstance(obj, Avatar):
            return False

        types = ['small', 'medium', 'large']
        return all(getattr(obj, t) == getattr(obj, t) for t in types)

    def __str__(self):
        return self.medium

    def __repr__(self):
        return f"<Avatar {self}>"


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
