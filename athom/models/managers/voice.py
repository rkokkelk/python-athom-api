import logging

from marshmallow import Schema, fields, post_load, EXCLUDE

log = logging.getLogger(__name__)


class Voice:

    def __init__(self, id=None, **kwargs):
        self.id = id

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f"Voice [{self.id}] {self.name}"


class VoiceSchema(Schema):
    sampleUrl = fields.Url

    class Meta:
        additional = ['id', 'name', 'language', 'locale', 'gender', 'installed']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Voice(**data)
