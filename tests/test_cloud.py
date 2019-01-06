import json
import urllib

import mock
import pytest
import responses

from athom.token import Token
from athom.cloud import AthomCloudAPI
from athom.storage.localstorage import LocalStorage
from athom.common.exceptions import AthomAPISessionError


class TestCloud:

    clientId = '988a9713388e1a7524be608e3554cffb9af9270e'
    clientSecret = '9b5c4e33b3d99f0ff8aef1e391d337e29e0b1c80'
    redirectUrl = 'https://localhost/api/callback'
    config = [clientId, clientSecret, redirectUrl]

    oauth= {
        "token_type":"bearer",
        "access_token":"3da881ff599c17128553662e2fb6e09cdbeec3bc",
        "expires_in":3660,
        "refresh_token":"5051b445460ee0680be4c5f39d67edfd2e277656"
    }


    @mock.patch('athom.storage.localstorage.LocalStorage')
    def test_api_init(self, mock_storage):
        api = AthomCloudAPI(*self.config)

        assert api.clientId == self.clientId
        assert api.clientSecret == self.clientSecret
        assert api.redirectUrl == self.redirectUrl
        assert api.token is not None
        assert api.storage is not None
        assert isinstance(api.storage, LocalStorage)
        assert mock_storage.get.called_once


    @responses.activate
    @mock.patch('athom.cloud.LocalStorage')
    def test_authentication_with_oauth(self, mock_storage):
        url = 'https://api.athom.com/oauth2/token'
        oath = '7d63b997e78277030a6f5b68ca9ff537224ea11f'

        responses.add(responses.POST, url, body=json.dumps(self.oauth))

        api = AthomCloudAPI(*self.config)
        token = api.authenticateWithAuthorizationCode(oath)

        request = responses.calls[0].request

        assert token == api.token
        assert mock_storage.set.called_once
        assert request.headers['Content-Type'] == 'application/x-www-form-urlencoded'
        assert 'grant_type=authorization_code' in request.body
        assert 'client_id='+self.clientId in request.body
        assert 'client_secret='+self.clientSecret in request.body

        for key, value in self.oauth.items():
            assert getattr(api.token, key) == value


    @responses.activate
    def test_api_authentication_fail(self):
        api = AthomCloudAPI(*self.config)
        api.setToken(Token(api))

        with pytest.raises(AthomAPISessionError):
            api.getUser()


    @responses.activate
    def test_api_get_user(self):
        url = 'https://api.athom.com/user/me'

        with open('tests/fixtures/user.json', 'r') as f:
            json_user = f.read()
            user_dict = json.loads(json_user)

        responses.add(responses.GET, url, body=json_user)

        api = AthomCloudAPI(*self.config)
        token = Token(api, **self.oauth)
        api.setToken(token)

        user = api.getUser()

        # Verify the GET request to Athom API
        request = responses.calls[0].request
        assert request.url == url
        assert request.headers['authorization'] == 'Bearer '+self.oauth['access_token']

        # Test user properties
        for column in ['lastname', 'firstname', 'email']:
            assert getattr(user, column) == user_dict[column]

        # Test the device properties
        for index, device in enumerate(user.devices):
            for column in ['name', 'token', 'platform']:
                assert getattr(device, column) == user_dict['devices'][index][column]

        # Test the avatar URL's
        avatar = user_dict['avatar']
        for column in avatar.keys():
            assert getattr(user.avatar, column) == avatar[column]

        # Test Homey object
        homey = user_dict['homeys'][0]
        for column in ['name', 'ipInternal', 'softwareVersion', 'language', 'state', 'role']:
            assert getattr(user.homeys[0], column) == homey[column]


    def test_api_check_authorization_code(self):
        api = AthomCloudAPI(*self.config)
        token = Token(api, **self.oauth)
        api.setToken(token)

        assert api.hasAuthorizationCode()

        token = Token(api)
        api.setToken(token)
        assert not api.hasAuthorizationCode()


    @mock.patch('athom.token.Token')
    def test_api_refresh_tokens(self, mock_token):
        api = AthomCloudAPI(*self.config)
        api.setToken(mock_token)

        api.refreshTokens()
        assert mock_token.refresh.called_once


    def test_api_get_login_url(self):
        api = AthomCloudAPI(*self.config)

        url = api.getLoginUrl()

        assert 'client_id='+self.clientId in url
        assert 'response_type=code' in url
        assert 'scopes=' in url


    def test_changing_auto_refresh_tokens(self):
        api = AthomCloudAPI(*self.config)

        api.disableAutoRefreshTokens()
        assert not api.autoRefreshTokens

        api.enableAutoRefreshTokens()
        assert api.autoRefreshTokens


    def test_set_token(self):
        api = AthomCloudAPI(*self.config)
        token = Token(api)

        api.setToken(token)
        assert api.token == token
