""":mod:`plastic.message` --- Request/response messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from werkzeug.wrappers import Request as BaseRequest, Response as BaseResponse

from .context import Context


class Request(BaseRequest):
    """The richier subclass of :class:`werkzeug.wrappers.Request`.

    :param environ: the wsgi environ to initialize with
    :type environ: :class:`collections.Mapping`
    :param app: the request app instance
    :type app: :class:`~plastic.app.BaseApp`
    :param endpoint: the requested endpoint
    :type endpoint: :class:`basestring`

    """

    #: (:class:`basestring`) The requested endpoint.
    endpoint = None

    #: (:class:`~plastic.app.BaseApp`) The requested application instance.
    app = None

    #: (:class:`~plastic.context.Context`) The context storage, which is
    #: a kind of :class:`dict`.  Keys can be accessed as like attributes.
    context = None

    def __init__(self, environ, app, endpoint, populate_request=True,
                 shallow=False):
        super(Request, self).__init__(environ=environ,
                                      populate_request=populate_request,
                                      shallow=shallow)
        self.endpoint = endpoint
        self.app = app
        self.context = Context()


class Response(BaseResponse):
    """The richier subclass of :class:`werkzeug.wrappers.Response`."""

