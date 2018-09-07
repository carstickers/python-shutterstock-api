from shutterstock import resources, configure_api


class API:
    def __init__(self, token):
        self.token = token

    def get(self, endpoint, **params):
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': 'Bearer {token}'.format(
                token=self.token
            )
        }

        endpoint = endpoint.format(**params)


def test_configure_api():
    api = configure_api(API('test'))
    assert issubclass(api.Image, resources.Image)
    assert issubclass(api.ImageCollection, resources.ImageCollection)
    assert issubclass(api.ImageLicense, resources.ImageLicense)
