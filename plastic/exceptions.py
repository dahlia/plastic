""":mod:`plastic.exceptions` --- Exception types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from werkzeug.exceptions import NotAcceptable


__all__ = 'PlasticError', 'RenderError'


class PlasticError(Exception):
    """All Plastic-related exceptions are derived from this class."""


class RenderError(PlasticError, NotAcceptable):
    """All rendering-related errors are derived from this class.
    It also extends :exc:`werkzeug.exceptions.NotAcceptable`.

    :param message: an optional error message for debugging purpose
    :param description: a message that will be showed to user agent

    """

    def __init__(self, message=None, description=None):
        super(RenderError, self).__init__(description)
        if message is not None:
            PlasticError.__init__(self, message)

