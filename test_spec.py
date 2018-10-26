from shutterstock.endpoint import EndPoint, EndPointParam, ChoicesParam, IntegerParam


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
    limit = IntegerParam(min=1, max=100)


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

    invalid_choice_raised = False
    try:
        uri, params = endpoint.prepare(id=5, choice='hard no')
    except ValueError:
        invalid_choice_raised = True
    assert invalid_choice_raised

    invalid_value_raised = False
    try:
        uri, params = endpoint.prepare(id=5, choice=EndPointParam.MAYBE, limit=0)
    except ValueError:
        invalid_value_raised = True
    assert invalid_value_raised

    invalid_value_raised = False
    try:
        uri, params = endpoint.prepare(id=5, choice=EndPointParam.MAYBE, limit=101)
    except ValueError:
        invalid_value_raised = True
    assert invalid_value_raised

    invalid_value_raised = False
    try:
        uri, params = endpoint.prepare(id=5, choice=EndPointParam.MAYBE,
                                       limit=100)
    except ValueError:
        invalid_value_raised = True
    assert invalid_value_raised is False

    invalid_value_raised = False
    try:
        uri, params = endpoint.prepare(id=5, choice=EndPointParam.MAYBE,
                                       limit=1)
    except ValueError:
        invalid_value_raised = True
    assert invalid_value_raised is False
