from shutterstock.endpoint import EndPoint, EndPointParam, ChoicesParam


class SimpleEndPoint(EndPoint):
    """Endpoint for testing"""
    YES = 'yes'
    NO = 'no'
    MAYBE = 'maybe'
    CHOICES = (YES, NO, MAYBE, )

    id = EndPointParam(required=True,
                       help_text='Required. The ID of the object.')
    choice = ChoicesParam(required=True, default=MAYBE, choices=CHOICES,
                           help_text='Required. Choice field')


def test_endpoint_param_setup():
    assert len(SimpleEndPoint.params) == 2
    assert SimpleEndPoint.id in SimpleEndPoint.params
    assert SimpleEndPoint.choice in SimpleEndPoint.params


def test_endpoint_prepare():
    endpoint = SimpleEndPoint('/simple/{id}')
    uri, params = endpoint.prepare(id=5, nothing=True, choice=SimpleEndPoint.NO)
    assert uri == '/simple/5'

    assert 'nothing' not in params

    assert 'id' in params
    assert params['id'] == 5
    assert 'choice' in params
    assert params['choice'] == SimpleEndPoint.NO
