from os.path import dirname, join

from attest import Tests, assert_hook

from plastic.config import Config


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

