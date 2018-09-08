import json
import requests


class ShutterstockAPI:
    def __init__(self, token):
        self.token = token

    @property
    def headers(self):
        return {
            'Content-Type': 'application/xml',
            'Authorization': 'Bearer {token}'.format(
                token=self.token
            )
        }

    def request(self, method, endpoint, **params):
        endpoint = endpoint.format(**params)

        response = method(
            'https://api.shutterstock.com/v2{endpoint}'.format(
                endpoint=endpoint
            ),
            params=params,
            headers=self.headers
        )
        print(json.loads(response.content))
        return json.loads(response.content)

    def get(self, endpoint, **params):
        return self.request(requests.get, endpoint, **params)

    def post(self, endpoint, **params):
        return self.request(requests.post, endpoint, **params)

    def put(self, endpoint, **params):
        return self.request(requests.put, endpoint, **params)

    def delete(self, endpoint, **params):
        return self.request(requests.delete, endpoint, **params)
