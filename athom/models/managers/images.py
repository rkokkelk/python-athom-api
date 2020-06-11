import logging

from marshmallow import Schema, post_load, EXCLUDE

log = logging.getLogger(__name__)


class Image:

    def __init__(self, id=None, **kwargs):
        self.id = id

        homey_url = kwargs.pop('homey_url', '')

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.fullUrl = homey_url + self.url

    def __eq__(self, obj):
        return isinstance(obj, Image) and obj.id == self.id

    def __str__(self):
        return self.url

    def __repr__(self):
        return f"<Image {self}>"


class ImageSchema(Schema):

    class Meta:
        additional = ['id', 'ownerUri', 'url', 'lastUpdated']
        unknown = EXCLUDE

    @post_load
    def create_obj(self, data):
        return Image(**data)
