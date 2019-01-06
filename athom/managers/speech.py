from athom.common import scopes
from athom.common.net import post

class ManagerSpeechInput:

    def __init__(self, homey, token):

        self.homey = homey
        self.homeyPath = "http://{homey.ip}/api/manager/speech-input".format(homey=homey)
        self.requiredScopes = scopes.HOMEY_SPEECH
        self.token = token


    def parseSpeech(self, transcript=None, **opts):
        url = self.homeyPath+"/"

        if not transcript:
            raise ValueError("Missing required transcript parameter")

        return post(url, json={'transcript': transcript, **opts}, token=self.token)


    def ask(self, text=None, **opts):
        url = self.homeyPath+"/ask"

        if not text:
            raise ValueError("Missing required text parameter")

        return post(url, json={'text': text, **opts}, token=self.token)
