from attest import Tests, assert_hook
from werkzeug.test import Client
from werkzeug.wrappers import Response

from plastic.message import Request
from plastic.app import BaseApp
from plastic.context import Context


App = BaseApp.clone()


tests = Tests()
app = App()
request = Request({}, app=app, endpoint='endpoint_name')


@tests.test
def app_():
    assert request.app is app


@tests.test
def endpoint():
    assert request.endpoint == 'endpoint_name'


@tests.test
def context():
    assert isinstance(request.context, Context)


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

