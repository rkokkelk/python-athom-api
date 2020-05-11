from athom.common import scopes
from athom.managers.manager import Manager
from athom.models.managers.voice import VoiceSchema


class ManagerSpeechOutput(Manager):

    def __init__(self, **kwargs):
        super().__init__(base='/speech-output', **kwargs)

        self.requiredScopes = scopes.HOMEY_SPEECH

    def say(self, **opts):
        if not opts.get('text'):
            raise ValueError("Missing required text parameter")

        return self.s.post('/say', json=opts)

    def getVoices(self, **opts):
        r = self.s.get('/voice/', params=opts)
        schema = VoiceSchema(many=True)
        return schema.load(r.text)

    def getVoice(self, **opts):
        id = opts.get('id')
        r = self.s.get(f"/voice/{id}")
        return VoiceSchema().load(r.json())

    def uninstallVoice(self, **opts):
        id = opts.get('id')
        return self.s.delete(f"/voice/{id}")

    def installVoice(self, **opts):
        id = opts.get('id')
        return self.s.post(f"/voice/{id}")

    def playVoiceSample(self, **opts):
        id = opts.get('id')
        return self.s.post(f"/voice/{id}/sample")

    def setOptionSpeed(self, **opts):
        if opts.get('value') not in ['very_slow', 'slow', 'normal'
                                     'fast', 'very_fast']:
            raise ValueError("Invalid option for value")

        return self.s.put('/option/speed', json=opts)

    def getOptionSpeed(self, **opts):
        return self.s.get('/option/speed')

    def setOptionVoice(self, **opts):
        return self.s.put('/option/voice', json=opts)

    def getOptionVoice(self, **opts):
        return self.s.get('/option/voice')
