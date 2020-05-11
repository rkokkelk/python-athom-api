import logging

from marshmallow import Schema, fields, post_load, EXCLUDE

log = logging.getLogger(__name__)


class Capability:

    def __init__(self, id=None, **kwargs):
        self.id = id

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, obj):
        return isinstance(obj, Capability) and obj.id == self.id

    def __str__(self):
        return f"[{self.type}] {self.title}"

    def __repr__(self):
        return f"<Capability {self}>"


class CapabilitySchema(Schema):

    desc = fields.Str(allow_none=True)
    units = fields.Str(allow_none=True)
    values = fields.List(fields.Dict)

    class Meta:
        additional = ['id', 'uri', 'title', 'type', 'getable', 'setable',
                      'charType', 'decimals', 'min', 'max', 'step']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Capability(**data)
