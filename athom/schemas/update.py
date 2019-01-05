from athom.models.update import Update
from marshmallow import Schema, fields, post_load, EXCLUDE

class UpdateSchema(Schema):
    version = fields.String()
    changelog = fields.Dict(values=fields.String(), keys=fields.String())
    channels = fields.List(fields.String())
    date = fields.DateTime()

    @post_load
    def create_obj(self, data):
        return Update(**data)
