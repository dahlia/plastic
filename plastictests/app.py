from attest import Tests, assert_hook, raises
from werkzeug.test import Client
from werkzeug.routing import Rule
from werkzeug.wrappers import Response

from plastic.app import BaseApp


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
    SimpleApp4 = BaseApp.clone('mod.name', 'SimpleApp4', test_attr=[1, 2, 3])
    assert issubclass(SimpleApp4, BaseApp)
    assert SimpleApp4.__module__ == 'mod.name'
    assert SimpleApp4.__name__ == 'SimpleApp4'
    assert SimpleApp4.test_attr == [1, 2, 3]


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
        return '[{0}] {1}, {2} {3}'.format(
            request.endpoint, name, request.method, request.path)
    App = BaseApp.clone()
    App.add_rule(Rule('/people/<name>', endpoint='test_person'), test_person)
    app = App()
    client = Client(app, Response)
    response = client.get('/people/hongminhee')
    assert response.status_code == 200
    assert response.data == '[test_person] hongminhee, GET /people/hongminhee'
    response = client.delete('/people/hongminhee')
    assert response.status_code == 200
    assert response.data == \
           '[test_person] hongminhee, DELETE /people/hongminhee'


@tests.test
def route():
    """BaseApp.route() method is a general decorator to add new
    routing rule.  It accepts the same arguments to werkzeug.routing.Rule
    and decorates a view function.

    """
    App = BaseApp.clone()
    @App.route('/people/<name>')
    def test_person(request, name):
        return '[{0}] {1}, {2} {3}'.format(
            request.endpoint, name, request.method, request.path)
    app = App()
    client = Client(app, Response)
    response = client.get('/people/hongminhee')
    assert response.status_code == 200
    assert response.data == '[test_person] hongminhee, GET /people/hongminhee'
    response = client.delete('/people/hongminhee')
    assert response.status_code == 200
    assert response.data == \
           '[test_person] hongminhee, DELETE /people/hongminhee'

