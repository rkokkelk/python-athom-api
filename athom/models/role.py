from marshmallow import Schema, fields, post_load, EXCLUDE

class Role:

    def __init__(self, _id=None, **kwargs):
        self._id = _id
        self.name = kwargs.pop('name', None)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return "[{self._id}] {self.name}".format(self=self)


class RoleSchema(Schema):

    # Exclude unknown keys
    class Meta:
        additional = ['_id', 'name', 'scopes']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Role(**data)
