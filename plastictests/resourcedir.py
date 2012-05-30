from attest import Tests, assert_hook, raises

from plastic.resourcedir import ResourceDirectory


tests = Tests()
rdir = ResourceDirectory(__name__, 'resources')


# $ tree plastictests/resources/
# plastictests/resources/
# ├── a
# ├── b
# ├── c
# │   ├── a
# │   ├── b
# │   ├── c
# │   │   └── a
# │   └── d
# └── d


@tests.test
def rdir_contains():
    assert 'a' in rdir
    assert 'b' in rdir
    assert 'c' in rdir
    assert 'c/a' in rdir
    assert 'c/b' in rdir
    assert 'c/c' in rdir
    assert 'c/c/a' in rdir
    assert 'c/c/b' not in rdir
    assert 'c/d' in rdir
    assert 'c/d/a' not in rdir
    assert 'c/e' not in rdir
    assert 'd' in rdir
    assert 'e' not in rdir


@tests.test
def rdir_getitem():
    with rdir['a'] as f:
        read = f.read().strip()
        assert read == 'a'
    with rdir['b'] as f:
        read = f.read().strip()
        assert read == 'b'
    assert isinstance(rdir['c'], ResourceDirectory)
    with rdir['c']['a'] as f:
        read = f.read().strip()
        assert read == 'c-a'
    with rdir['c']['b'] as f:
        read = f.read().strip()
        assert read == 'c-b'
    assert isinstance(rdir['c']['c'], ResourceDirectory)
    with rdir['c']['c']['a'] as f:
        read = f.read().strip()
        assert read == 'c-c-a'
    with rdir['c/a'] as f:
        read = f.read().strip()
        assert read == 'c-a'
    with rdir['c/b'] as f:
        read = f.read().strip()
        assert read == 'c-b'
    assert isinstance(rdir['c/c'], ResourceDirectory)
    with rdir['c/c/a'] as f:
        read = f.read().strip()
        assert read == 'c-c-a'
    with raises(KeyError):
        rdir['c/c/b']
    assert isinstance(rdir['c/d'], ResourceDirectory)
    with raises(KeyError):
        rdir['c/e']
    assert isinstance(rdir['d'], ResourceDirectory)
    with raises(KeyError):
        rdir['e']


@tests.test
def rdir_iter():
    expected = set(['a', 'b', 'c', 'c/a', 'c/b', 'c/c', 'c/c/a', 'c/d', 'd'])
    assert set(rdir) == expected
    assert set(rdir['c']) == set(['a', 'b', 'c', 'c/a', 'd'])
    assert set(rdir['c']['c']) == set(['a'])
    assert set(rdir['c/c']) == set(['a'])


@tests.test
def rdir_len():
    assert len(rdir) == 9
    assert len(rdir['c']) == 5
    assert len(rdir['c']['c']) == 1
    assert len(rdir['c/c']) == 1
    assert len(rdir['d']) == 0

