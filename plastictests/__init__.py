from attest import Tests

from plastic.version import VERSION, VERSION_INFO
from . import app, context


tests = Tests()
tests.register(app.tests)
tests.register(context.tests)


@tests.test
def version():
    assert map(int, VERSION.split('.')) == list(VERSION_INFO)

