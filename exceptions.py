class RequeststError(Exception):
    """Error requests."""
    pass


class StatusNot200Error(Exception):
    """Ststus.code return != 200."""
    pass


class DataNotDictError(TypeError):
    """When data is not dict."""
    pass


class DataNotLictError(TypeError):
    """When data is not list."""
    pass


class NotKeyError(KeyError):
    """When no key."""
    pass


class SentError(Exception):
    """When message not sent"""
    pass
