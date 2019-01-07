from athom.managers.apps import ManagerApps
from athom.managers.speech import ManagerSpeechInput

class HomeyAPI:

    def __init__(self, ipInternal, token):

        self.ip = ipInternal
        self.token = token

        self.ManagerApps = ManagerApps(homey=self, token=token)
        self.ManagerSpeechInput = ManagerSpeechInput(homey=self, token=token)


    def forCurrentHomey(self):
        raise NotImplementedError("HomeyAPI cannot be used locally!")
