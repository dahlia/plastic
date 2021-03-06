from attest import Tests, assert_hook
from werkzeug.test import Client, EnvironBuilder
from werkzeug.wrappers import Response

from plastic.message import Request
from plastic.app import BaseApp
from plastic.context import Context


App = BaseApp.clone()


@App.route('/')
def endpoint_name(request):
    return request.build_url('build_url_test', a=1, b=2, c=3)


@App.route('/<int:a>/<int:b>')
def build_url_test(request, a, b):
    return repr((a, b))


tests = Tests()
app = App()

request = Request(EnvironBuilder().get_environ(), app=app)


@tests.test
def app_():
    assert request.app is app


@tests.test
def endpoint():
    assert request.endpoint == 'endpoint_name'


@tests.test
def context():
    assert isinstance(request.context, Context)


@tests.test
def build_url():
    client = Client(App(), Response)
    response = client.get('/')
    assert response.data == '/1/2?c=3'


@App.route('/session', methods=['POST'])
def set_session(request):
    request.session['val'] = [1, 2, 3]
    return ''


@App.route('/session', methods=['GET'])
def get_session(request):
    current = repr(request.session['val'])
    request.session['val'] += [request.session['val'][-1] + 1]
    return current


@tests.test
def session():
    client = Client(App(), Response)
    client.post('/session')
    body = client.get('/session').data.strip()
    assert body == '[1, 2, 3]'
    body = client.get('/session').data.strip()
    assert body == '[1, 2, 3, 4]'
    body = client.get('/session').data.strip()
    assert body == '[1, 2, 3, 4, 5]'


@tests.test
def session_cookie_key():
    app = App()
    assert (app.session_cookie['key'] ==
            app.config['session_cookie']['key'] ==
            'sessionid')
    app2 = App(config={'session_cookie': {'key': 'my_session_id'}})
    assert (app2.session_cookie['key'] ==
            app2.config['session_cookie']['key'] ==
            'my_session_id')

