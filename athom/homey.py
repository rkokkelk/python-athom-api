from athom.managers.apps import ManagerApps
from athom.managers.users import ManagerUsers
from athom.managers.devices import ManagerDevices
from athom.managers.sessions import ManagerSessions
from athom.managers.speechInput import ManagerSpeechInput
from athom.managers.speechOutput import ManagerSpeechOutput


class HomeyAPI:

    def __init__(self, url, token):
        self.url = url

        # Use delegationToken to create sessionToken to access API
        self.users = ManagerUsers(homey=self)
        # Ensure to get a valid Session
        self.token = self.users.login(token)

        manager_options = {
            'homey': self,
            'token': self.token
        }

        self.apps = ManagerApps(**manager_options)
        self.devices = ManagerDevices(**manager_options)
        self.session = ManagerSessions(**manager_options)
        self.speechInput = ManagerSpeechInput(**manager_options)
        self.speechOutput = ManagerSpeechOutput(**manager_options)

    def forCurrentHomey(self):
        raise NotImplementedError("This function is not supported by this module")
