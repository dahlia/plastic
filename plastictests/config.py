from os.path import dirname, join

from attest import Tests, assert_hook, raises

from plastic.app import BaseApp
from plastic.config import (Config, config_property, get_typename,
                            import_instance)


tests = Tests()


@tests.test
def update_from_object():
    class config_object:
        debug = True
        database_uri = 'sqlite://'
        _hidden = 123
    config = Config()
    config.update_from_object(config_object)
    assert config['debug'] is True
    assert config['database_uri'] == 'sqlite://'
    assert '_hidden' not in config
    # should not overwrite
    config['debug'] = False
    del config['database_uri']
    config.update_from_object(config_object)
    assert config['debug'] is False
    assert config['database_uri'] == 'sqlite://'
    # should overwrite
    config['debug'] = False
    del config['database_uri']
    config.update_from_object(config_object, overwrite=True)
    assert config['debug'] is True
    assert config['database_uri'] == 'sqlite://'


@tests.test
def update_from_file():
    config_filename = join(dirname(__file__), 'test.cfg')
    config = Config()
    config.update_from_file(config_filename)
    assert config['debug'] is True
    assert config['database_uri'] == 'sqlite://'
    assert '_hidden' not in config
    # should not overwrite
    config['debug'] = False
    del config['database_uri']
    config.update_from_file(config_filename)
    assert config['debug'] is False
    assert config['database_uri'] == 'sqlite://'
    # should overwrite
    config['debug'] = False
    del config['database_uri']
    config.update_from_file(config_filename, overwrite=True)
    assert config['debug'] is True
    assert config['database_uri'] == 'sqlite://'


@tests.test
def update_unless_exists():
    config = Config(a=1, b=2, c=3)
    config.update_unless_exists({'b': 1, 'd': 2, 'e': 3}, c=4, f=5)
    assert dict(config) == {'a': 1, 'b': 2, 'c': 3, 'd': 2, 'e': 3, 'f': 5}


@tests.test
def repr_():
    assert repr(Config()) == 'plastic.config.Config()'
    assert repr(Config(a=1)) == 'plastic.config.Config(a=1)'
    assert repr(Config({'is': 1})) == "plastic.config.Config({'is': 1})"
    assert (repr(Config({'a': 1, 'is': 2})) ==
            "plastic.config.Config({'is': 2}, a=1)")


class ConfigTestApp(BaseApp):
    """Test app."""

    conf_attr = config_property('conf_attr')


@tests.test
def config_property_():
    app = ConfigTestApp({'conf_attr': 123})
    assert app.conf_attr == 123


@tests.test
def import_instance_():
    instance = import_instance('plastic.config:Config', Config)
    assert isinstance(instance, Config)
    instance = import_instance('plastic.config:Config()', Config)
    assert isinstance(instance, Config)
    instance = import_instance('plastic.config:Config(a=1, b=bare)', Config)
    assert isinstance(instance, Config)
    assert len(instance) == 2
    assert instance['a'] == 1
    assert instance['b'] == 'bare'
    instance = import_instance('plastic.config:Config(pi = 3.14)', Config)
    assert len(instance) == 1
    assert instance['pi'] == 3.14
    instance = import_instance('plastic.config:Config(null = None)', Config)
    assert len(instance) == 1
    assert instance['null'] is None
    instance = import_instance('plastic.config:Config(a=True, b=False)', dict)
    assert len(instance) == 2
    assert instance['a'] is True
    assert instance['b'] is False
    instance = import_instance('plastic.config:Config(a="True", b=\'b\')', dict)
    assert len(instance) == 2
    assert instance['a'] == 'True'
    assert instance['b'] == 'b'
    with raises(ValueError):
        import_instance('plastic.config:Config(a=1, 2)', Config)
    with raises(ValueError):
        import_instance('plastic.config:Config(', Config)
    with raises(ValueError):
        import_instance('plastic.config:Config(a,)', Config)
    with raises(ValueError):
        import_instance('plastic.config:Config(a=2 + 1)', Config)
    with raises(ValueError):
        import_instance('plastic.config:Config(a=f())', Config)
    with raises(ValueError):
        import_instance('plastic.config:Config(a=[1, 2])', Config)


@tests.test
def get_typename_():
    assert get_typename(Config) == 'plastic.config.Config'
    assert get_typename(xrange) == 'xrange'

