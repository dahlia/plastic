""":mod:`plastic.config` --- Configuration mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from keyword import iskeyword
from re import compile
from tokenize import Name

__all__ = 'Config',


class Config(dict):
    """Mapping object (subtype of :class:`dict`) to store configurations."""

    def update_unless_exists(self, mapping=(), **keywords):
        """Almost equivalent to :meth:`~dict.update()` except
        it ignores keys already exist.

        >>> config = Config(a=1, b=2)
        >>> config.update({'b': 1, 'c': 2})
        >>> config
        plastic.config.Config(a=1, b=2, c=3)

        """
        if callable(getattr(mapping, 'keys', None)):
            for key in mapping:
                if key not in self:
                    self[key] = mapping[key]
        else:
            for key, value in mapping:
                if key not in self:
                    self[key] = value
        for key, value in keywords.iteritems():
            if key not in self:
                self[key] = value

    def __repr__(self):
        cls = type(self)
        typename = cls.__module__ + '.' + cls.__name__
        is_ident = compile('^' + Name + '$').match
        keywords = []
        literals = []
        format_keyword = '{0}={1!r}'.format
        format_literal = '{0!r}: {1!r}'.format
        for key, value in self.iteritems():
            if is_ident(key) and not iskeyword(key):
                keywords.append(format_keyword(key, value))
            else:
                literals.append(format_literal(key, value))
        keywords = ', '.join(keywords)
        literals = ', '.join(literals)
        if literals and keywords:
            return '{0}({{{1}}}, {2})'.format(typename, literals, keywords)
        elif literals:
            return '{0}({{{1}}})'.format(typename, literals)
        return '{0}({1})'.format(typename, keywords)

