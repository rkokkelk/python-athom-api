import json

class Token:

    def __init__(self, access_token=None, expires_in=-1, token_type="bearer", refresh_token=None):
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.refresh_token = refresh_token


    @staticmethod
    def generate_token(json_str):
        token = Token()
        data = json.loads(json_str)

        for key, value in data.items():
            setattr(token, key, value)

        return token
