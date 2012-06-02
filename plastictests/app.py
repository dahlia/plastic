import warnings

from attest import Tests, assert_hook, raises
from werkzeug.test import Client
from werkzeug.routing import Rule
from werkzeug.wrappers import Response

from plastic.app import BaseApp
from plastic.exceptions import RenderError
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
def render_template():
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
    @App.route('/one')
    def one(request):
        return request.app.render_template(
            request, 'render_template_one.html',
            {'a': 'hello'}, b=123
        )
    @App.route('/two')
    def two(request):
        return request.app.render_template(
            request, 'render_template_two.html',
            {'a': 'world'}, b=456
        )
    error = [None]
    @App.route('/three')
    def three(request):
        try:
            return request.app.render_template(request,
                                               'render_template_three.html')
        except RenderError as e:
            error[0] = e
            raise
    client = Client(App(), Response)
    response = client.get('/one')
    assert response.status_code == 200
    assert response.data.strip() == 't1: /one, hello, 123'
    response = client.get('/two')
    assert response.status_code == 200
    assert (response.data.strip() ==
            "t2: <Request 'http://localhost/two' [GET]>, world, 456")
    response = client.get('/three')
    assert response.status_code == 406
    assert isinstance(error[0], RenderError)

