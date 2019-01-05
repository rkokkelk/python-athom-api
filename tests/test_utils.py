from athom.common import utils

class TestUtils:


    def test_generate_url(self):
        base_url = 'https://10.10.10.10:443'

        params = {
            'param1': 'value1',
            'param2': 'value2'
        }

        url = utils.create_url(base_url, params)
        assert url == 'https://10.10.10.10:443/?param1=value1&param2=value2'
