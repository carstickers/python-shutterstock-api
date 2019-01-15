
class APIError(Exception):
    pass


class APIRedirectError(APIError):
    pass


class APIClientError(APIError):
    pass


class APIServerError(APIError):
    pass
