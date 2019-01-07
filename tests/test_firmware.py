import pytest
import responses

from datetime import datetime
from requests.exceptions import ConnectionError, SSLError

from athom.models.update import Update
from athom.firmware import AthomFirmwareAPI
from athom.common.exceptions import AthomAPIConnectionError


class TestFirmware:

    @classmethod
    def setup(cls):
        with open('tests/fixtures/firmware_changelog.json', 'r') as f:
            json = f.read()

        responses.add(responses.GET, 'https://firmware.athom.com/api/update/changelog',
                      body=json)


    @responses.activate
    def test_firmware_api(self):
        api = AthomFirmwareAPI()
        updates = api.getUpdatesChangelog()

        assert len(updates) == 15
        assert updates[0] > updates[14]

        for update in updates:
            assert update.changelog is not None
            assert update.version is not None
            assert update.date is not None
            assert update.channels is not None

            assert len(update.languages()) == 1
            assert update.languages()[0] == 'en'


    @responses.activate
    def test_firmware_change_basepath(self):
        url = 'http://10.001.102.203'
        api = AthomFirmwareAPI(baseUrl=url)

        with pytest.raises(AthomAPIConnectionError):
            api.getUpdatesChangelog()

        assert responses.calls[0].request.url == url+'/update/changelog'


    @responses.activate
    def test_firmware_models(self):
        api = AthomFirmwareAPI()
        updates = api.getUpdatesChangelog()

        update = updates[0]
        assert update.version == '2.0.0-rc.9'
        assert 'public beta of Homey v2.0!' in update.changelog['en']
        assert len(update.channels) == 1
        assert update.channels == ['beta']
        assert update.date == datetime.strptime('2018-12-21T19:43:22Z', '%Y-%m-%dT%H:%M:%SZ')

        update = updates[14]
        assert update.version == '1.1.2'
        assert 'userdata folder to Homey' in update.changelog['en']
        assert len(update.channels) == 2
        assert update.channels == ['stable', 'beta']
        assert update.date == datetime.strptime('2016-12-30T15:52:44Z', '%Y-%m-%dT%H:%M:%SZ')


    def test_firmware_objects_comparison(self):
        nones = {'changelog': None, 'channels': None, 'date': None}

        assert Update('2.0.0', **nones) < Update('2.0.0-rc1', **nones)
        assert Update('2.0.0-rc1', **nones) < Update('2.0.0-rc10', **nones)
        assert Update('1.5.20-rc18', **nones) < Update('2.0.0', **nones)
        assert Update('1.5.20-rc18', **nones) == Update('1.5.20-rc18', **nones)
