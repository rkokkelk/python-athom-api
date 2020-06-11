from athom.common import scopes
from athom.managers.manager import Manager
from athom.models.managers.images import ImageSchema


class ManagerImages(Manager):

    def __init__(self, **kwargs):
        super().__init__(base='/images', **kwargs)

        self.requiredScopes = [
            scopes.HOMEY_DEVICE
        ]

    def getImages(self):
        r = self.s.get('/image')
        schema = ImageSchema(many=True)
        return schema.load(r.json().values())

    def getImage(self, **opts):
        id = opts.get('id')
        r = self.s.get(f'/image/{id}')
        return ImageSchema().load(r.json())
