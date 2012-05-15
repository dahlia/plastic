from attest import Tests, assert_hook, raises

from plastic.context import Context


tests = Tests()


@tests.test
def context_get():
    list_ = []
    context = Context(number=123, string='abc', list_=list_)
    assert context.number == context['number'] == 123
    assert 'number' in context
    assert hasattr(context, 'number')
    assert context.string == context['string'] == 'abc'
    assert 'string' in context
    assert hasattr(context, 'string')
    assert context.list_ is context['list_'] is list_
    assert 'list_' in context
    assert hasattr(context, 'list_')
    assert 'nokey' not in context
    assert not hasattr(context, 'noattr')
    with raises(KeyError):
        context['nokey']
    with raises(AttributeError):
        context.noattr


@tests.test
def context_set():
    context = Context()
    context.abc = 123
    assert context.abc == context['abc'] == 123
    context['def_'] = 456
    assert context.def_ == context['def_'] == 456


@tests.test
def context_del():
    context = Context(abc=123, def_=456)
    del context['abc']
    assert 'abc' not in context
    del context.def_
    assert 'def_' not in context

