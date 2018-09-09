from shutterstock import resources, configure_api
from shutterstock.resources import ImageEndPoint


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


client = configure_api(API('test'))


def test_configure_api_client():
    assert issubclass(client.Image, resources.Image)
    assert issubclass(client.ImageCollection, resources.ImageCollection)
    assert issubclass(client.ImageLicense, resources.ImageLicense)


def test_endpoint_param_format():
    assert client.Image.GET.format(id=5) == '/images/5'


def test_endpoint_param_explain():
    img_ep = ImageEndPoint('/images')
    assert img_ep.explain().startswith('/images')
