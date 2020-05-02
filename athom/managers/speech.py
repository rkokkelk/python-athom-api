from athom.common import scopes
from athom.managers.manager import Manager


class ManagerSpeechInput(Manager):

    def __init__(self, **kwargs):
        super().__init__(base='/speech-input', **kwargs)

        self.requiredScopes = scopes.HOMEY_SPEECH

    def parseSpeech(self, transcript=None, **opts):
        if not transcript:
            raise ValueError("Missing required transcript parameter")

        return self.s.post('/', json={'transcript': transcript, **opts})

    def ask(self, text=None, **opts):
        if not text:
            raise ValueError("Missing required text parameter")

        return self.s.post('/ask', json={'text': text, **opts})
