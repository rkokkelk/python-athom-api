import sys
import pytest
import logging
import configparser

from pprint import pprint
from marshmallow.exceptions import ValidationError

from athom.common import utils
from athom.token import Token
from athom.cloud import AthomCloudAPI

log = logging.getLogger()

def setup_logging(debug=False):

    default_formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d [%(levelname)-.1s]: %(message)s",
        "%H:%M:%S"
    )

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(default_formatter)

    if debug:
        log.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)

    log.addHandler(ch)

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

        setup_logging(debug=True)

    @pytest.mark.integration
    def test_integration(self):
        api = AthomCloudAPI(self.clientId, self.clientSecret, self.returnUrl)

        if not api.hasAuthorizationCode():
            log.warning(api.getLoginUrl())
            api.authenticateWithAuthorizationCode(self.oath)
            return

        user = api.getUser()
        log.info(user)

        for role in user.roles:
            log.info(role)

        homey = user.getFirstHomey()
        log.info(homey)

        homeyAPI = homey.authenticate()

        mApps = homeyAPI.apps
        for app in mApps.getApps():
            log.info(app)

        mApps.installFromAppStore('net.weejewel.xboxone')
        mApps.uninstallApp('net.weejewel.xboxone')

        raise Exception()
