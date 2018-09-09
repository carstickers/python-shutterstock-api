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


def test_endpoint_params():
    assert len(SimpleEndPoint.params) == 2
    assert SimpleEndPoint.id in SimpleEndPoint.params
    assert SimpleEndPoint.choice in SimpleEndPoint.params
