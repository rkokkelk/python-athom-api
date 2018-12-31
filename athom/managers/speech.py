from athom.common.scopes import homeySpeech
from athom.common.utils import get, json

class ManagerSpeechInput:

    def __init__(self, homey, token):

        self.homey = homey
        self.homeyPath = "http://{homey.ip}/api/manager/speech-input".format(homey=homey)
        self.requiredScopes = homeySpeech()
        self.token = token


    def parseSpeech(self, transcript=None, **opts):
        url = self.homeyPath+"/"

        if not transcript:
            raise ValueError("Missing required transcript parameter")

        return json(url, data={'transcript': transcript, **opts}, token=self.token)


    def ask(self, text=None, **opts):
        url = self.homeyPath+"/ask"

        if not text:
            raise ValueError("Missing required text parameter")

        return json(url, data={'text': text, **opts}, token=self.token)
