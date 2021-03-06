import json
import requests

from shutterstock.exceptions import APIRedirectError, APIClientError, \
    APIServerError, InvalidAPIResponseError


class ShutterstockAPI:
    def __init__(self, token):
        self.token = token

    @property
    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {token}'.format(
                token=self.token
            )
        }

    def request(self, method, endpoint, data_key='params', **params):
        endpoint, params = endpoint.prepare(**params)
        data = {
            data_key: params
        }

        response = method(
            'https://api.shutterstock.com/v2{endpoint}'.format(
                endpoint=endpoint
            ),
            headers=self.headers,
            **data
        )
        status = response.status_code // 100

        try:
            response_content = json.loads(response.content.decode('utf-8'))
        except Exception:
            raise InvalidAPIResponseError(response.content, response.status_code)

        if status == 2:
            return response_content
        elif status == 3:
            raise APIRedirectError(response_content['message'], response.status_code)
        elif status == 4:
            raise APIClientError(response_content['message'], response.status_code)
        elif status == 5:
            raise APIServerError(response_content['message'], response.status_code)

        raise InvalidAPIResponseError(response_content, response.status_code)

    def get(self, endpoint, **params):
        return self.request(requests.get, endpoint, **params)

    def post(self, endpoint, **params):
        return self.request(requests.post, endpoint, data_key='json', **params)

    def put(self, endpoint, **params):
        return self.request(requests.put, endpoint, data_key='json', **params)

    def delete(self, endpoint, **params):
        return self.request(requests.delete, endpoint, **params)
