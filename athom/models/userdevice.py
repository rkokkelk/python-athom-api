from marshmallow import Schema, fields, post_load, EXCLUDE

class UserDevice:

    def __init__(self, _id=None, **kwargs):
        self._id = _id
        self.name = kwargs.pop('name', None)
        self.platform = kwargs.pop('platform', None)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f"[{self._id}] {self.name} ({self.platform})"


class UserDeviceSchema(Schema):

    class Meta:
        additional = ['_id', 'name', 'platform', 'token', 'publicKey', 'appVersion'
                      'created', 'updated', 'devMode']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return UserDevice(**data)
