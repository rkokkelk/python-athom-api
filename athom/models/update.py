import logging

log = logging.getLogger(__name__)

class Update:

    def __init__(self, version, changelog, channels, date):
        self.version = version
        self.changelog = changelog
        self.channels = channels
        self.date = date


    def languages(self):
        return self.changelog.keys()


    def __str__(self):
        return "Update {self.version}".format(self=self)
