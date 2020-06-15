from athom.common.net import AthomSession
from athom.managers.apps import ManagerApps
from athom.managers.images import ManagerImages
from athom.managers.devices import ManagerDevices
from athom.managers.sessions import ManagerSessions
from athom.managers.speechInput import ManagerSpeechInput
from athom.managers.speechOutput import ManagerSpeechOutput
from athom.managers.users import ManagerUsers


class HomeyAPI:

    def __init__(self, url, token):
        self.url = url

        # Use delegationToken to create sessionToken to access API
        # Ensure to get a valid Session
        self.token = ManagerUsers(homey=self).login(token)

        manager_options = {
            'homey': self,
            'token': self.token
        }

        self.apps = ManagerApps(**manager_options)
        self.images = ManagerImages(**manager_options)
        self.devices = ManagerDevices(**manager_options)
        self.session = ManagerSessions(**manager_options)
        self.speechInput = ManagerSpeechInput(**manager_options)
        self.speechOutput = ManagerSpeechOutput(**manager_options)
        self.users = ManagerUsers(**manager_options)

        # Set request.Session for API interaction
        self.s = AthomSession(token=self.token, base=self.url)

    def forCurrentHomey(self):
        raise NotImplementedError("This function is not supported by this module")
