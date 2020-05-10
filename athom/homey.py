from athom.managers.apps import ManagerApps
from athom.managers.users import ManagerUsers
from athom.managers.sessions import ManagerSessions
from athom.managers.speech import ManagerSpeechInput


class HomeyAPI:

    def __init__(self, url, token):
        self.url = url

        # Use delegationToken to create sessionToken to access API
        self.users = ManagerUsers(homey=self)
        # Ensure to get a valid Session
        self.token = self.ManagerUsers.login(token)

        manager_options = {
            'homey': self,
            'token': self.token
        }

        self.apps = ManagerApps(**manager_options)
        self.session = ManagerSessions(**manager_options)
        self.speechInput = ManagerSpeechInput(**manager_options)

    def forCurrentHomey(self):
        raise NotImplementedError("This function is not supported by this module")
