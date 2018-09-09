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
    not_required = EndPointParam(help_text='This field is not required.')


def test_endpoint_param_setup():
    assert len(SimpleEndPoint.params) == 3
    assert SimpleEndPoint.id in SimpleEndPoint.params
    assert SimpleEndPoint.choice in SimpleEndPoint.params
    assert SimpleEndPoint.not_required in SimpleEndPoint.params


def test_endpoint_prepare():
    endpoint = SimpleEndPoint('/simple/{id}')
    uri, params = endpoint.prepare(id=5, nothing=True)
    assert uri == '/simple/5'

    assert 'nothing' not in params

    assert 'id' in params
    assert params['id'] == 5

    # Test default on require field
    assert 'choice' in params
    assert params['choice'] == SimpleEndPoint.MAYBE

    # Test that not_required is not in params list
    assert 'not_required' not in params
