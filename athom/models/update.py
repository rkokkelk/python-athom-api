import logging

log = logging.getLogger(__name__)

class Update:

    def __init__(self, version, changelog, channels, date):
        self.version = version
        self.changelog = changelog
        self.channels = channels
        self.date = date


    def languages(self):
        return list(self.changelog.keys())


    def __str__(self):
        return "Update {self.version}".format(self=self)


    def __eq__(self, other):
        return self.version == other.version


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
