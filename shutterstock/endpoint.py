

class EndPointParam:
    def __init__(self):
        self.value = None


class EndPoint:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def format(self, params):
        return self.endpoint.format(**params)
