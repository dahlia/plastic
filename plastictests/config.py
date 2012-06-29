from attest import Tests, assert_hook

from plastic.config import Config


tests = Tests()


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

