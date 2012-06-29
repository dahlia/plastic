from attest import Tests

from plastic.version import VERSION, VERSION_INFO
from . import app, config, context, message, rendering, resourcedir


tests = Tests()
tests.register(app.tests)
tests.register(config.tests)
tests.register(context.tests)
tests.register(message.tests)
tests.register(rendering.tests)
tests.register(resourcedir.tests)


@tests.test
def version():
    """VERSION_INFO should be a tuple like (1, 2, 3) and
    VERSION should be a string like '1.2.3'.

    """
    assert map(int, VERSION.split('.')) == list(VERSION_INFO)

