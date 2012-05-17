from attest import Tests, assert_hook

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

