from marshmallow import Schema, post_load, EXCLUDE


class Role:

    def __init__(self, _id=None, **kwargs):
        self._id = _id
        self.name = kwargs.pop('name', None)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, obj):
        return isinstance(obj, Role) and obj._id == self._id

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Role {self}>"


class RoleSchema(Schema):

    # Exclude unknown keys
    class Meta:
        additional = ['_id', 'name', 'scopes']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Role(**data)
