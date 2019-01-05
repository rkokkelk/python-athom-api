import json
import mock
import responses

from athom.token import Token

class TestToken:

    data = {
        'access_token': '22cf4225ed0f778efe168b22d0d4563be13b92e6',
        'refresh_token': '7f9c28ce80401faadb314ec659df415ddb047498',
        'token_type': 'bearer',
        'expires_in': 10000
    }

    @mock.patch('athom.cloud.AthomCloudAPI')
    def test_token_init(self, mock_api):
        token = Token(mock_api, **self.data)

        for key, value in self.data.items():
            assert getattr(token, key) == value

        assert str(token) == self.data['access_token']


    @mock.patch('athom.cloud.AthomCloudAPI')
    def test_token_jsonify(self, mock_api):
        token = Token(mock_api, **self.data)
        assert self.data == token.jsonify()


    @mock.patch('athom.cloud.AthomCloudAPI')
    def test_generate_token(self, mock_api):
        token = Token.generate_token(mock_api, json.dumps(self.data))

        for key, value in self.data.items():
            assert getattr(token, key) == value

        assert str(token) == self.data['access_token']


    @responses.activate
    @mock.patch('athom.cloud.AthomCloudAPI')
    def test_token_auto_refresh(self, mock_api):
        url = 'https://api.athom.com/oauth2/token'
        oauth_json = {
            "token_type":"bearer",
            "access_token":"2da881ff599c17128553662e2fb6e09cdbeec3bc",
            "expires_in":3660,
            "refresh_token":"5051b445460ee0680be4c5f39d67edfd2e277656"
        }

        token = Token(mock_api, **self.data)
        responses.add(responses.POST, url, body=json.dumps(oauth_json))

        token.refresh()
        for key, value in oauth_json.items():
            assert getattr(token, key) == value

        request = responses.calls[0].request

        assert request.url == url
        assert request.headers['Content-Type'] == 'application/x-www-form-urlencoded'
        assert 'grant_type=refresh_token' in request.body
        assert 'refresh_token='+self.data['refresh_token'] in request.body
