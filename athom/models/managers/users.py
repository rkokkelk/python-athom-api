import logging

from marshmallow import Schema, fields, post_load, EXCLUDE

log = logging.getLogger(__name__)


class User:

    def __init__(self, id=None, **kwargs):
        self.id = id

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, obj):
        return isinstance(obj, User) and obj.id == self.id

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<User {self}>"


class UserSchema(Schema):

    asleep = fields.Bool(allow_none=True)

    class Meta:
        additional = ['id', 'name', 'athomId', 'properties', 'enabled',
                      'verified', 'role', 'present']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return User(**data)
