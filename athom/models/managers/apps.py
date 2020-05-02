from marshmallow import Schema, fields, post_load, EXCLUDE

class Apps:

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)


    def __str__(self):
        return "{self.id}".format(self=self)


class AppsSchema(Schema):

    # Specify vars which can have None values
    crashedMessage = fields.Str(allow_none=True)
    exitCode = fields.Int(allow_none=True)
    exitSignal = fields.Str(allow_none=True)

    # Exclude unknown keys
    class Meta:
        additional = ['id', 'sdk', 'enabled', 'autoupdate', 'name', 'origin', 'channel',
                      'version', 'compatibility', 'icon', 'iconObj', 'author', 'permissions',
                      'session', 'ready', 'images', 'state', 'exitCounty', 'settings', 'brandColor',
                      'hasDrivers', 'usage', 'hasUpdates']

        ordered = True
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Apps(**data)
