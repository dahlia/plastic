from attest import Tests

from plastic.version import VERSION, VERSION_INFO
from . import app, context


tests = Tests()
tests.register(app.tests)
tests.register(context.tests)


@tests.test
def version():
    """VERSION_INFO should be a tuple like (1, 2, 3) and
    VERSION should be a string like '1.2.3'.

    """
    assert map(int, VERSION.split('.')) == list(VERSION_INFO)

