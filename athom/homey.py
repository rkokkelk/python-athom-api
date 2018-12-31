from athom.managers.speech import ManagerSpeechInput

class HomeyAPI:

    def __init__(self, ipInternal, token):

        self.ip = ipInternal
        self.token = token

        self.ManagerSpeechInput = ManagerSpeechInput(self, token=token)


    def forCurrentHomey(self):
        raise NotImplementedError("HomeyAPI cannot be used locally!")
