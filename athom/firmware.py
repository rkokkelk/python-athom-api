import json
import logging

from athom.common.net import get
from athom.models.update import Update, UpdateSchema

log = logging.getLogger(__name__)

class AthomFirmwareAPI:

    def __init__(self, baseUrl=None):
        self.basePath = 'https://firmware.athom.com/api' if not baseUrl else baseUrl


    def getUpdatesChangelog(self):
        r = get(self.basePath+'/update/changelog')

        schema = UpdateSchema(many=True)
        updates = schema.load(json.loads(r)['message']['updates'])

        log.info("Gathered %d updates", len(updates))
        return updates
