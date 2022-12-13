class RequeststError(Exception):
    """Error requests."""
    pass


class StatusNot200(Exception):
    """Ststus.code return != 200."""
    pass


class DataNotDict(TypeError):
    """When data is not dict."""
    pass


class DataNotLict(TypeError):
    """When data is not list."""
    pass


class ErrorNotKey(KeyError):
    """When no key."""
    pass


class ErrorSent(Exception):
    """When message not sent"""
    pass
