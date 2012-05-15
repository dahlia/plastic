from attest import Tests, assert_hook, raises

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

