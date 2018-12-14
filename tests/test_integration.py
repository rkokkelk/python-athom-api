import logging
import configparser

from homey import utils
from homey.token import Token
from homey.cloud import AthomCloudAPI

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

    def test_integration(self):
        api = AthomCloudAPI(self.clientId, self.clientSecret, self.returnUrl)

        api.authenticateWithAuthorizationCode(self.oath)

        api.getUser()
