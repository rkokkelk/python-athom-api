from athom.common import scopes
from athom.common.net import post
from athom.managers.manager import Manager

class ManagerSpeechInput(Manager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.path = "http://{homey.ip}/api/manager/speech-input".format(homey=self.homey)
        self.requiredScopes = scopes.HOMEY_SPEECH


    def parseSpeech(self, transcript=None, **opts):
        url = self.path+"/"

        if not transcript:
            raise ValueError("Missing required transcript parameter")

        return post(url, json={'transcript': transcript, **opts}, token=self.token)


    def ask(self, text=None, **opts):
        url = self.path+"/ask"

        if not text:
            raise ValueError("Missing required text parameter")

        return post(url, json={'text': text, **opts}, token=self.token)
