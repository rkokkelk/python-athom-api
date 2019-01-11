from athom.managers.apps import ManagerApps
from athom.managers.speech import ManagerSpeechInput

class HomeyAPI:

    def __init__(self, ipInternal, token):

        self.ip = ipInternal
        self.token = token

        self.apps = ManagerApps(homey=self, token=token)
        self.SpeechInput = ManagerSpeechInput(homey=self, token=token)


    def forCurrentHomey(self):
        raise NotImplementedError("This function is not supported by this module")
