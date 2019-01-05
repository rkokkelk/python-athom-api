import json
import mock
import pytest
import responses

from requests.exceptions import SSLError

from athom.common.net import get, post
from athom.common.exceptions import AthomCloudAuthenticationError, \
                                    AthomCloudGateWayAPIError, \
                                    AthomCloudUnknownAPIError, \
                                    AthomAPIConnectionError


class TestNet:


    @responses.activate
    def test_get_request(self):
        # Test normal GET request
        responses.add(responses.GET, 'http://localhost/api')
        get('http://localhost/api', params={'param1':'foobar', 'param2': 2})
        assert responses.calls[0].request.url == 'http://localhost/api?param1=foobar&param2=2'


    @responses.activate
    def test_get_request_connection_errors(self):
        with pytest.raises(AthomAPIConnectionError, match=r'.*Connection refused.*') as e:
            get('http://localhost/api/2', params={'param1':'foobar', 'param2': 2})

        responses.add(responses.GET, 'http://localhost/api/changelog', body=SSLError())
        with pytest.raises(AthomAPIConnectionError) as e:
            get('http://localhost/api/changelog', params={'param1':'foobar', 'param2': 2})


    @responses.activate
    def test_get_request_api_errors(self):
        data = {'code': 503, 'error':'unknown', 'error_description':'unknown error'}
        responses.add(responses.GET, 'http://localhost/api', body=json.dumps(data), status=503)

        with pytest.raises(AthomCloudUnknownAPIError, match=r'\[503\].*unknown error.*'):
            get('http://localhost/api', params={'param1':'foobar', 'param2': 2})

        assert responses.calls[0].request.url == 'http://localhost/api?param1=foobar&param2=2'

        responses.add(responses.GET, 'http://localhost/api2', body='Bad Gateway', status=502)
        with pytest.raises(AthomCloudGateWayAPIError, match=r'\[502\].*bad gateway.*'):
            get('http://localhost/api2', params={'param1':'foobar', 'param2': 2})

        assert responses.calls[1].request.url == 'http://localhost/api2?param1=foobar&param2=2'


    @responses.activate
    @mock.patch('athom.token.Token')
    def test_get_request_authentication_errors(self, mock_token):
        data = {'code': 401, 'error':'invalid_auth', 'error_description':'Invalid authentication'}
        responses.add(responses.GET, 'http://localhost/api', status=401, body=json.dumps(data))

        # Test authentication issues without token and refresh
        with pytest.raises(AthomCloudAuthenticationError, match=r'\[401\].*Invalid authentication.*'):
            get('http://localhost/api', refresh=False, params={'param1':'foobar', 'param2': 2})

        assert responses.calls[0].request.url == 'http://localhost/api?param1=foobar&param2=2'
        assert not mock_token.refresh.called

        # Test authenitcation issues with token without refresh
        with pytest.raises(AthomCloudAuthenticationError, match=r'\[401\].*Invalid authentication.*'):
            get('http://localhost/api', token=mock_token, refresh=False, params={'param1':'foobar', 'param2': 2})

        assert responses.calls[1].request.url == 'http://localhost/api?param1=foobar&param2=2'
        assert not mock_token.refresh.called

        # Test authentication with token and refresh enabled
        with pytest.raises(AthomCloudAuthenticationError, match=r'\[401\].*Invalid authentication.*'):
            get('http://localhost/api', token=mock_token, params={'param1':'foobar', 'param2': 2})

        assert responses.calls[2].request.url == 'http://localhost/api?param1=foobar&param2=2'
        assert responses.calls[3].request.url == 'http://localhost/api?param1=foobar&param2=2'
        assert mock_token.refresh.called_once


    @responses.activate
    def test_post_request(self):
        # Test normal POST request
        responses.add(responses.POST, 'http://localhost/api')
        post('http://localhost/api', json={'param1':'foobar', 'param2': 2})
        assert responses.calls[0].request.url == 'http://localhost/api'


    @responses.activate
    def test_post_request_connection_errors(self):
        with pytest.raises(AthomAPIConnectionError, match=r'.*Connection refused.*') as e:
            post('http://localhost/api/2', json={'param1':'foobar', 'param2': 2})

        responses.add(responses.POST, 'http://localhost/api/changelog', body=SSLError())
        with pytest.raises(AthomAPIConnectionError) as e:
            post('http://localhost/api/changelog', json={'param1':'foobar', 'param2': 2})


    @responses.activate
    def test_post_request_api_errors(self):
        data = {'code': 503, 'error':'unknown', 'error_description':'unknown error'}
        responses.add(responses.POST, 'http://localhost/api', body=json.dumps(data), status=503)

        with pytest.raises(AthomCloudUnknownAPIError, match=r'\[503\].*unknown error.*'):
            post('http://localhost/api', json={'param1':'foobar', 'param2': 2})

        assert responses.calls[0].request.url == 'http://localhost/api'

        responses.add(responses.POST, 'http://localhost/api2', body='Bad Gateway', status=502)
        with pytest.raises(AthomCloudGateWayAPIError, match=r'\[502\].*bad gateway.*'):
            post('http://localhost/api2', json={'param1':'foobar', 'param2': 2})

        assert responses.calls[1].request.url == 'http://localhost/api2'


    @responses.activate
    @mock.patch('athom.token.Token')
    def test_post_request_authentication_errors(self, mock_token):
        data = {'code': 401, 'error':'invalid_auth', 'error_description':'Invalid authentication'}
        responses.add(responses.POST, 'http://localhost/api', status=401, body=json.dumps(data))

        # Test authentication issues without token and refresh
        with pytest.raises(AthomCloudAuthenticationError, match=r'\[401\].*Invalid authentication.*'):
            post('http://localhost/api', refresh=False, json={'param1':'foobar', 'param2': 2})

        assert responses.calls[0].request.url == 'http://localhost/api'
        assert not mock_token.refresh.called

        # Test authenitcation issues with token without refresh
        with pytest.raises(AthomCloudAuthenticationError, match=r'\[401\].*Invalid authentication.*'):
            post('http://localhost/api', token=mock_token, refresh=False, json={'param1':'foobar', 'param2': 2})

        assert responses.calls[1].request.url == 'http://localhost/api'
        assert not mock_token.refresh.called

        # Test authentication with token and refresh enabled
        with pytest.raises(AthomCloudAuthenticationError, match=r'\[401\].*Invalid authentication.*'):
            post('http://localhost/api', token=mock_token, json={'param1':'foobar', 'param2': 2})

        assert responses.calls[2].request.url == 'http://localhost/api'
        assert responses.calls[3].request.url == 'http://localhost/api'
        assert mock_token.refresh.called_once
