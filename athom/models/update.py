import logging

from marshmallow import Schema, fields, post_load, EXCLUDE

log = logging.getLogger(__name__)


class Update:

    def __init__(self, version=None, **kwargs):
        self.version = version
        self.changelog = kwargs.pop('changelog', dict())

        for key, value in kwargs.items():
            setattr(self, key, value)

    def languages(self):
        return list(self.changelog.keys())

    def __str__(self):
        return self.version

    def __repr__(self):
        return f"<Update {self}>"

    def __eq__(self, obj):
        return isinstance(obj, Update) and self.version == obj.version

    def __lt__(self, other):
        s_split = self.version.split('-rc')
        o_split = other.version.split('-rc')

        # 2.0.0-rc1 < 2.0.0
        if s_split[0] == o_split[0]:

            # 2.0.0-rc1 < 2.0.0-rc20
            if len(s_split) == 2 and len(o_split) == 2:
                return int(s_split[1]) < int(o_split[1])

            else:
                return self.version < other.version

        else:
            # 1.5.3 < 2.0.0-rc10
            return self.version < other.version

    def __gt__(self, other):
        s_split = self.version.split('-rc')
        o_split = other.version.split('-rc')

        # 2.0.0-rc1 > 2.0.0
        if s_split[0] == o_split[0]:

            # 2.0.0-rc1 > 2.0.0-rc20
            if len(s_split) == 2 and len(o_split) == 2:
                return int(s_split[1]) > int(o_split[1])

            else:
                return self.version > other.version

        else:
            # 1.5.3 > 2.0.0-rc10
            return self.version > other.version


class UpdateSchema(Schema):
    date = fields.DateTime()

    class Meta:
        additional = ['version', 'changelog', 'channels']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Update(**data)
