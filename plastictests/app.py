import warnings

from attest import Tests, assert_hook, raises
from werkzeug.test import Client
from werkzeug.routing import Rule
from werkzeug.wrappers import Response

from plastic.app import BaseApp
from plastic.exceptions import RenderError
from plastic.rendering import render_template
from plastic.warnings import AppWarning


tests = Tests()

SimpleApp = BaseApp.clone()  # STORE_NAME


@tests.test
def app_clone():
    """BaseApp.clone() method is a shorthand of subclassing.
    It should automatically set subclass' __name__ and __module__
    attributes.

    """
    global SimpleApp2
    assert issubclass(SimpleApp, BaseApp)
    assert SimpleApp.__module__ == __name__
    assert SimpleApp.__name__ == 'SimpleApp'
    SimpleApp2 = BaseApp.clone('mod.name')  # STORE_GLOBAL
    assert issubclass(SimpleApp2, BaseApp)
    assert SimpleApp2.__module__ == 'mod.name'
    assert SimpleApp2.__name__ == 'SimpleApp2'
    SimpleApp3 = BaseApp.clone('mod.name')  # STORE_FAST
    assert issubclass(SimpleApp3, BaseApp)
    assert SimpleApp3.__module__ == 'mod.name'
    assert SimpleApp3.__name__ == 'SimpleApp3'
    SimpleApp4 = BaseApp.clone('mod.name', 'SimpleApp4',
                               template_path='views/')
    assert issubclass(SimpleApp4, BaseApp)
    assert SimpleApp4.__module__ == 'mod.name'
    assert SimpleApp4.__name__ == 'SimpleApp4'
    assert SimpleApp4.template_path == 'views/'


@tests.test
def warn_baseapp_init():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        BaseApp()
        assert issubclass(w[0].category, AppWarning)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        BaseApp.clone()()
        assert len(w) == 0


@tests.test
def config():
    """Each application instance should have their own (isolated each other)
    configuration.

    """
    app1 = SimpleApp({'a': 1})
    app2 = SimpleApp({'b': 2})
    assert app1.config['a'] == 1
    assert 'b' not in app1.config
    assert app2.config['b'] == 2
    assert 'a' not in app2.config
    @app1.config.update_from_object
    class test_config:
        b = 3
    assert app1.config['b'] == 3
    assert app2.config['b'] == 2


@tests.test
def wsgi():
    """Instances of BaseApp (or its subtypes) should be WSGI compliant."""
    app = SimpleApp()
    client = Client(app, Response)
    response = client.get('/not-exist')
    assert response.status_code == 404


@tests.test
def add_rule():
    """BaseApp.add_rule() method is a primitive method to add new
    routing rule.  It accepts werkzeug.routing.Rule and view function
    to map each other.

    """
    def test_person(request, name):
        assert request.app._id == 'test'
        assert request.endpoint == 'test_person'
        return '[{0}] {1}, {2} {3}'.format(
            request.endpoint, name, request.method, request.path)
    App = BaseApp.clone()
    App.add_rule(Rule('/people/<name>', endpoint='test_person'), test_person)
    app = App()
    app._id = 'test'
    client = Client(app, Response)
    response = client.get('/people/hongminhee')
    assert response.status_code == 200
    assert response.data == '[test_person] hongminhee, GET /people/hongminhee'
    response = client.delete('/people/hongminhee')
    assert response.status_code == 200
    assert response.data == \
           '[test_person] hongminhee, DELETE /people/hongminhee'


@tests.test
def add_template_engine():
    def t1(request, path, values):
        return 't1: ' + repr((request, path, values))
    def t2(request, path, values):
        return 't2: ' + repr((request, path, values))
    App = BaseApp.clone()
    App.add_template_engine('t1', t1)
    App.add_template_engine('t2', t2)
    assert not BaseApp.template_engines
    assert len(App.template_engines) == 2
    assert App.template_engines['t1'] is t1
    assert App.template_engines['t2'] is t2
    with raises(ValueError):
        App.add_template_engine('t2', t2)
    with raises(TypeError):
        App.add_template_engine('t3', 1234)


@tests.test
def add_serializer():
    def s1(request, value):
        return 's1: ' + repr((request, value))
    def s2(request, value):
        return 's2: ' + repr((request, value))
    App = BaseApp.clone()
    App.add_serializer('application/x-s1', s1)
    App.add_serializer('application/x-s2', s2)
    assert not BaseApp.mimetype_mapping
    assert len(App.mimetype_mapping) == 2
    assert App.mimetype_mapping['application/x-s1'] is s1
    assert App.mimetype_mapping['application/x-s2'] is s2
    with raises(ValueError):
        App.add_serializer('application/x-s2', s2)
    with raises(TypeError):
        App.add_serializer('application/x-s3', 1234)


@tests.test
def associate_mimetypes():
    App = BaseApp.clone()
    App.associate_mimetypes(html='text/html', xml='text/xml')
    App.associate_mimetypes({'text/plain': 'md', 'text/x-markdown': 'md'})
    assert not BaseApp.mimetype_mapping
    assert len(App.mimetype_mapping) == 4
    assert App.mimetype_mapping['text/html'] == 'html'
    assert App.mimetype_mapping['text/xml'] == 'xml'
    assert App.mimetype_mapping['text/plain'] == 'md'
    assert App.mimetype_mapping['text/x-markdown'] == 'md'
    with raises(TypeError):
        App.associate_mimetypes()
    with raises(TypeError):
        App.associate_mimetypes([1, 2])
    with raises(ValueError):
        App.associate_mimetypes(xhtml='text/html')
    with raises(ValueError):
        App.associate_mimetypes({'text/plain': 'txt'})


@tests.test
def route():
    """BaseApp.route() method is a general decorator to add new
    routing rule.  It accepts the same arguments to werkzeug.routing.Rule
    and decorates a view function.

    """
    App = BaseApp.clone()
    @App.route('/people/<name>')
    def test_person(request, name):
        assert request.app._id == 'test'
        assert request.endpoint == 'test_person'
        return '[{0}] {1}, {2} {3}'.format(
            request.endpoint, name, request.method, request.path)
    app = App()
    app._id = 'test'
    client = Client(app, Response)
    response = client.get('/people/hongminhee')
    assert response.status_code == 200
    assert response.data == '[test_person] hongminhee, GET /people/hongminhee'
    response = client.delete('/people/hongminhee')
    assert response.status_code == 200
    assert response.data == \
           '[test_person] hongminhee, DELETE /people/hongminhee'


@tests.test
def template_engine():
    App = BaseApp.clone()
    @App.template_engine('t1')
    def t1(request, path, values):
        return 't1: ' + repr((request, path, values))
    @App.template_engine('t2')
    def t2(request, path, values):
        return 't2: ' + repr((request, path, values))
    assert not BaseApp.template_engines
    assert len(App.template_engines) == 2
    assert App.template_engines['t1'] is t1
    assert App.template_engines['t2'] is t2


@tests.test
def serializer():
    App = BaseApp.clone()
    @App.serializer('application/x-s1')
    def s1(request, value):
        return 's1: ' + repr((request, value))
    @App.serializer(['application/x-s2', 'application/x-s3'])
    def s2(request, value):
        return 's2: ' + repr((request, value))
    assert not BaseApp.mimetype_mapping
    assert len(App.mimetype_mapping) == 3
    assert App.mimetype_mapping['application/x-s1'] is s1
    assert App.mimetype_mapping['application/x-s2'] is s2
    assert App.mimetype_mapping['application/x-s3'] is s2


@tests.test
def render_template_():
    App = BaseApp.clone()
    @App.template_engine('t1')
    def t1(request, path, values):
        with request.app.template_directory[path] as template:
            return template.read().format(request=request, **values)
    @App.template_engine('t2')
    def t2(request, path, values):
        context = {'request': request}
        context.update(values)
        with request.app.template_directory[path] as template:
            return template.read() % context
    for way in 'app', 'helper':
        if way == 'app':
            def get_func(request):
                return request.app.render_template
        elif way == 'helper':
            def get_func(request):
                return render_template
        else:
            assert False, 'something wrong'
        @App.route('/' + way + '/one')
        def one(request):
            return get_func(request)(
                request, 'render_template_one.html',
                {'a': 'hello'}, b=123
            )
        @App.route('/' + way + '/two')
        def two(request):
            return get_func(request)(
                request, 'render_template_two.html',
                {'a': 'world'}, b=456
            )
        error = [None]
        @App.route('/' + way + '/three')
        def three(request):
            try:
                return get_func(request)(request,
                                         'render_template_three.html')
            except RenderError as e:
                error[0] = e
                raise
    for way in 'app', 'helper':
        client = Client(App(), Response)
        response = client.get('/' + way + '/one')
        assert response.status_code == 200, way
        assert response.data.strip() == 't1: /' + way +'/one, hello, 123', way
        response = client.get('/' + way + '/two')
        assert response.status_code == 200, way
        assert (response.data.strip() ==
                "t2: <Request 'http://localhost/" + way + "/two' [GET]>, "
                'world, 456'), way
        response = client.get('/' + way + '/three')
        assert response.status_code == 406, way
        assert isinstance(error[0], RenderError), way


@tests.test
def view_returns_string():
    App = BaseApp.clone()
    @App.route('/str')
    def return_str(request):
        return 'okay str'
    @App.route('/unicode')
    def return_unicode(request):
        return u'okay \uc720\ub2c8\ucf54\ub4dc'
    client = Client(App(), Response)
    response = client.get('/str')
    assert response.status_code == 200
    assert response.data == 'okay str'
    response = client.get('/unicode')
    assert response.status_code == 200
    expected = 'okay \xec\x9c\xa0\xeb\x8b\x88\xec\xbd\x94\xeb\x93\x9c'
    assert response.data == expected
