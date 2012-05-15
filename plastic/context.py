""":mod:`plastic.context` --- Contexts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections


class Context(dict, collections.MutableMapping):
    """The simple context storage which is a subtype of :class:`dict`.
    It works in similar way except keys can be accessed via its attributes.
    For example, the following lines are::

        assert isinstance(ctxt, plastic.context.Context)
        ctxt.user_id = 123
        user_id = ctxt.user_id
        del ctxt.user_id

    equivalent to::

        ctxt['user_id'] = 123
        user_id = ctxt['user_id']
        del ctxt['user_id']

    .. note::

       You can't access reserved attribute names like :meth:`dict.get`,
       :meth:`dict.setdefault`.  To use these names you have to use
       index operator::

           ctxt['setdefault']

    """

    def __getattr__(self, attribute):
        try:
            return self[attribute]
        except KeyError:
            raise AttributeError('no attribute ' + repr(attribute))

    def __setattr__(self, attribute, value):
        self[attribute] = value

    def __delattr__(self, attribute):
        try:
            del self[attribute]
        except KeyError:
            raise AttributeError('no attribute ' + repr(attribute))

