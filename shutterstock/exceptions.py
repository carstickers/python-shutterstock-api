
class APIError(Exception):
    message = None
    status_code = None
    content = None

    def __init__(self, message, status_code, content):
        self.message = message
        self.status_code = status_code
        self.content = content


class APIRedirectError(APIError):
    pass


class APIClientError(APIError):
    pass


class APIServerError(APIError):
    pass


class InvalidAPIResponseError(APIError):
    pass