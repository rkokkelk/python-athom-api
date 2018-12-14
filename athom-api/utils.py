import requests

def post(url, data):
    r = requests.post(
        url=url,
        data=data
    )

    if not r.response_code:
        raise Exception()

    return r.text
