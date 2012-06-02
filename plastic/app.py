""":mod:`plastic.app` --- Application factories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from __future__ import absolute_import

import dis
import itertools
import sys
import warnings

from werkzeug.datastructures import ImmutableDict
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map, RequestRedirect, Rule
from werkzeug.serving import run_simple

from .exceptions import RenderError
from .message import Request, Response
from .resourcedir import ResourceDirectory
from .warnings import AppWarning


class BaseApp(object):
    """The application base class.  In order to make an application
    you have to inherit this class.  As you know Python's subclassing
    can be done like::

        from plastic.app import BaseApp

        class MyApp(BaseApp):
            pass

    However in most cases you don't have to fill its body but
    simply :meth:`clone()`::

        from plastic.app import BaseApp

        MyApp = BaseApp.clone()

    Use :meth:`route()` class method for routing.

    """

    #: (:class:`collections.Mapping`) The :class:`dict` of endpoints to
    #: view functions.
    endpoints = {}

    #: (:class:`collections.Sequence`) The list of routing rules.
    rules = []

    #: (:class:`basestring`) The path to the directory which
    #: contains template files.  It has to be relative to the application
    #: module.  It can be overridden.  Default is :file:`templates/`.
    template_path = 'templates/'

    #: (:class:`~werkzeug.datastructures.ImmutableDict`) The immutable
    #: dictionary of suffix to registered templating functions.
    template_engines = ImmutableDict()

    @classmethod
    def clone(cls, __module__=None, __name__=None, **values):
        """Subclasses the application class.  It is a just shorthand of
        normal subclassing.  If your application becomes bigger stop
        using this and normaly subclass the application class
        using :keyword:`class` keyword instead.

        """
        try:
            getframe = sys._getframe
        except AttributeError:
            pass
        else:
            frame = getframe(1)
            if __module__ is None:
                __module__ = frame.f_globals.get('__name__')
            if __name__ is None:
                code = frame.f_code.co_code[frame.f_lasti:]
                code = code[3 if ord(code[0]) >= dis.HAVE_ARGUMENT else 1:]
                stores = (dis.opmap['STORE_NAME'],
                          dis.opmap['STORE_GLOBAL'],
                          dis.opmap['STORE_FAST'])
                opcode = ord(code[0])
                if opcode in stores:
                    name_pos = ord(code[1])
                    if opcode == dis.opmap['STORE_FAST']:
                        index = frame.f_code.co_varnames
                    else:
                        index = frame.f_code.co_names
                    try:
                        __name__ = index[name_pos]
                    except IndexError:
                        pass
        if __name__ is None:
            __name__ = 'App'
        subclass = type(__name__, (cls,), values)
        subclass.__module__ = __module__
        return subclass

    @classmethod
    def add_rule(cls, rule, function):
        """Adds a new ``rule`` and maps it to the ``function``.
        It is a lower-level primitive method.  In most cases you
        don't need it and just use :meth:`route()` decorator or
        other higher-level methods.

        :param rule: the rule to add
        :type rule: :class:`werkzeug.routing.Rule`
        :param function: the function to map to the ``rule``
        :type function: :class:`collections.Callable`

        """
        if not isinstance(rule, Rule):
            raise TypeError('rule must be a werkzeug.routing.Rule instance')
        elif not callable(function):
            raise TypeError('function must be callable')
        if getattr(cls, 'initialized_app_class', None) is not cls:
            cls.endpoints = cls.endpoints.copy()
            cls.rules = cls.rules[:]
            cls.initialized_app_class = cls
        cls.rules.append(rule)
        cls.endpoints[rule.endpoint] = function

    @classmethod
    def add_template_engine(cls, suffix, function):
        """Registers a templating ``function`` to the given ``suffix``.
        The function should take three arguments and returns its rendering
        result:

        .. function:: add_template_engine.function(request, path, values):

           :param request: the current request object
           :type request: :class:`~plastic.message.Request`
           :param path: the path of the template file.  it can be a key
                        of :attr:`~BaseApp.template_directory` mapping
                        object
           :type path: :class:`basestring`
           :param values: the values to be passed to the template
           :type values: :class:`collections.Mapping`
           :returns: the rendering result
           :rtype: :class:`basestring`

        :param suffix: the filename suffix (without period character)
                       to register the template engine e.g. ``'mako'``
        :type suffix: :class:`basestring`
        :param function: templating function.  see also :func:`function()`
                         for its signature
        :type function: :class:`collections.Callable`

        """
        if not callable(function):
            raise TypeError('function must be callable, but ' +
                            repr(function) + ' seems not')
        if suffix in cls.template_engines:
            raise ValueError('suffix ' + repr(suffix) + ' already exists')
        copy = cls.template_engines.iteritems()
        rest = [(suffix, function)]
        cls.template_engines = ImmutableDict(itertools.chain(copy, rest))

    @classmethod
    def route(cls, *rule_args, **rule_kwargs):
        """The function decorator which maps the path to the decorated
        view function.

        It takes the same arguments to the constructor of
        :class:`werkzeug.routing.Rule` class.  In most case simply give
        a path string to route::

            @App.route('/people/<name>')
            def person(request, name):
                return 'Hi, ' + name

        """
        rule = Rule(*rule_args, **rule_kwargs)
        def decorate(function):
            if rule.endpoint is None:
                try:
                    rule.endpoint = function.__name__
                except AttributeError:
                    raise TypeError(
                        'function has to be an ordinary function (not just '
                        'callable) or endpoint has to be specified'
                    )
            cls.add_rule(rule, function)
            return function
        return decorate

    @classmethod
    def template_engine(cls, suffix):
        """The function decorator which makes the given ``function``
        the template engine of the ``suffix``.
        ::

            # The following example has several issues.  Do not C&P
            # it into your program.
            from mako.template import Template

            @App.template_engine(suffix='mako')
            def render_mako(request, path, values):
                with request.app.template_directory[path] as f:
                    template = Template(f.read())
                return template.render(**values)

        :param suffix: the filename suffix (without period character)
                       to register the template engine e.g. ``'mako'``
        :type suffix: :class:`basestring`

        """
        def decorate(function):
            cls.add_template_engine(suffix, function)
            return function
        return decorate

    def __init__(self):
        cls = type(self)
        if cls is BaseApp:
            warnings.warn('you probably wanted to BaseApp.clone() instead of '
                          'making an instance of BaseApp',
                          category=AppWarning, stacklevel=2)
        self.endpoints = self.endpoints.copy()
        self.routing_map = Map(self.rules, strict_slashes=True)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        """The actual WSGI function.  Replace it when the application
        should be wrapped by middlewares.
        ::

            app.wsgi_app = Middleware(app.wsgi_app)

        """
        bound = self.routing_map.bind_to_environ(environ)
        try:
            try:
                endpoint, values = bound.match()
            except RequestRedirect as result:
                pass
            else:
                try:
                    view_func = self.endpoints[endpoint]
                except KeyError:
                    result = NotFound()
                else:
                    request = Request(environ, app=self, endpoint=endpoint)
                    result = view_func(request, **values)
                    if isinstance(result, str):
                        result = Response(result)
        except HTTPException as result:
            pass
        response = Response.force_type(result, environ)
        return response(environ, start_response)

    @property
    def template_directory(self):
        """(:class:`~plastic.resourcedir.ResourceDirectory`) The mapping
        object of the template directory.

        """
        return ResourceDirectory(type(self).__module__, self.template_path)

    def render_template(self, request, path, values={}, **keywords):
        """Renders the response using registered :attr:`template_engines`.

        :param request: a request which make it to render
        :type request: :class:`~plastic.message.Request`
        :param path: a path to template files without specific suffix
        :type path: :class:`basestring`
        :param values: a dictionary of values to pass to template
        :type values: :class:`collections.Mapping`
        :param \*\*keywords: the same to ``values`` except these are passed
                             by keywords
        :returns: a rendered result
        :rtype: :class:`basestring`
        :raises plastic.exceptions.RenderError:
           when there are no matched template files

        """
        directory = self.template_directory
        try:
            dirname, basename = path.rsplit('/', 1)
        except ValueError:
            dirname = ''
            basename = path
        else:
            dirname += '/'
            directory = directory[dirname]
        apply_name = (basename + '.').__add__
        for suffix, render in self.template_engines.iteritems():
            applied_name = apply_name(suffix)
            if applied_name in directory:
                break
        else:
            raise RenderError('no matched template files: ' + path)
        values = values.copy()
        values.update(keywords)
        return render(request, dirname + applied_name, values)

    def run(self, host='127.0.0.1', port=5555, debug=True, **options):
        """Starts serving the application.

        :param host: the hostname to listen.  default is ``'127.0.0.1'``
                     (localhost)
        :type host: :class:`basestring`
        :param port: the port number to listen.  default is 5555
        :type port: :class:`int`
        :param debug: use debugger and reloader.  default is ``True``
        :type debug: :class:`bool`
        :param \*\*options: other options to be passed to
                            :func:`werkzeug.routing.run_simple()` function

        """
        options.setdefault('use_reloader', debug)
        options.setdefault('use_debugger', debug)
        options.setdefault('use_evalex', debug)
        run_simple(hostname=host, port=port, application=self, **options)

