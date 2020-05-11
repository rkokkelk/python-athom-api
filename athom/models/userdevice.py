from marshmallow import Schema, fields, post_load, EXCLUDE

class UserDevice:

    def __init__(self, _id=None, **kwargs):
        self._id = _id
        self.name = kwargs.pop('name', None)
        self.platform = kwargs.pop('platform', None)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, obj):
        return isinstance(obj, UserDevice) and obj._id == self._id

    def __str__(self):
        return f"{self.name}({self.platform})"

    def __repr__(self):
        return f"<UserDevice {self}>"


class UserDeviceSchema(Schema):

    class Meta:
        additional = ['_id', 'name', 'platform', 'token', 'publicKey', 'appVersion'
                      'created', 'updated', 'devMode']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return UserDevice(**data)
