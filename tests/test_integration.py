import pytest
import logging
import configparser

from athom.common import utils
from athom.token import Token
from athom.cloud import AthomCloudAPI

log = logging.getLogger(__name__)

class TestIntegration:

    clientId = None
    clientSecret = None
    oath = None
    returnUrl = None

    @classmethod
    def setup(cls):
        config = configparser.ConfigParser()
        config.read('tests/api_test.cfg')

        if not config:
            log.critical("Unittest API config file not found: api_test.cfg")

        cls.clientId = config.get('credentials', 'clientId')
        cls.clientSecret = config.get('credentials', 'clientSecret')
        cls.oath = config.get('credentials', 'OATH2TOKEN')
        cls.returnUrl = config.get('credentials', 'callback')

        utils.setup_logging(debug=True)

    @pytest.mark.integration
    def test_integration(self):
        api = AthomCloudAPI(self.clientId, self.clientSecret, self.returnUrl)

        if not api.hasAuthorizationCode():
            print(api.getLoginUrl())
            api.authenticateWithAuthorizationCode(self.oath)

            return

        user = api.getUser()
        print(user)

        for role in user.roles:
            print(role)

        print(user.avatar.small)

        for device in user.devices:
            print(device)

        homey = user.getFirstHomey()
        print(homey)
        print(homey.geolocation)

        print(homey.users)

        homeyAPI = homey.authenticate()

        homeyAPI.ManagerSpeechInput.parseSpeech(transcript='foobar')
        print(homeyAPI.ManagerApps.getApps())
