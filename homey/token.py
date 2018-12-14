class Token:

    token_type = None
    expires_in = -1
    access_token = None

    def __init__(self, access_token, expires_in, token_type="bearer"):
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type


    def refresh_token(self):
        raise Exception("Not implemented yet")
