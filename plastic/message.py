""":mod:`plastic.message` --- Request/response messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from werkzeug.utils import cached_property
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

    #: (:class:`werkzeug.routing.MapAdapter`) The bound url adapter.
    bound_routing_map = None

    #: (:class:`collections.Mapping`) The pararmeter values of routed
    #: endpoint.
    endpoint_values = None

    #: (:class:`~plastic.context.Context`) The context storage, which is
    #: a kind of :class:`dict`.  Keys can be accessed as like attributes.
    context = None

    def __init__(self, environ, app, populate_request=True, shallow=False):
        super(Request, self).__init__(environ=environ,
                                      populate_request=populate_request,
                                      shallow=shallow)
        self.bound_routing_map = app.routing_map.bind_to_environ(environ)
        self.endpoint, self.endpoint_values = self.bound_routing_map.match()
        self.app = app
        self.context = Context()

    @cached_property
    def session(self):
        """(:class:`collections.MutableMapping`) The session storage.
        If this value has changed in view functions the state will be
        kept in future requests of the same session as well.

        """
        app = self.app
        sid = self.cookies.get(app.session_cookie['key'])
        store = app.session_store
        if sid:
            return store.get(sid)
        return store.new()


class Response(BaseResponse):
    """The richier subclass of :class:`werkzeug.wrappers.Response`."""

