from attest import Tests, assert_hook, raises

from plastic.app import BaseApp


tests = Tests()

SimpleApp = BaseApp.clone()


@tests.test
def app_clone():
    global SimpleApp2
    assert issubclass(SimpleApp, BaseApp)
    assert SimpleApp.__module__ == __name__
    assert SimpleApp.__name__ == 'SimpleApp'
    SimpleApp2 = BaseApp.clone('mod.name')
    assert issubclass(SimpleApp2, BaseApp)
    assert SimpleApp2.__module__ == 'mod.name'
    assert SimpleApp2.__name__ == 'SimpleApp2'
    SimpleApp3 = BaseApp.clone('mod.name')
    assert issubclass(SimpleApp3, BaseApp)
    assert SimpleApp3.__module__ == 'mod.name'
    assert SimpleApp3.__name__ == 'SimpleApp3'
    SimpleApp4 = BaseApp.clone('mod.name', 'SimpleApp4', test_attr=[1, 2, 3])
    assert issubclass(SimpleApp4, BaseApp)
    assert SimpleApp4.__module__ == 'mod.name'
    assert SimpleApp4.__name__ == 'SimpleApp4'
    assert SimpleApp4.test_attr == [1, 2, 3]

