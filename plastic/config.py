""":mod:`plastic.config` --- Configuration mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from keyword import iskeyword
from re import compile
from os.path import abspath
from tokenize import Name
from types import ModuleType

from werkzeug.utils import import_string

__all__ = 'Config',


class Config(dict):
    """Mapping object (subtype of :class:`dict`) to store configurations."""

    def update_from_object(self, object_, overwrite=False):
        """Updates configuration from arbitrary ``object_``.
        ::

            @config.update_from_object
            class default_config:
                debug = False
                database_uri = 'sqlite://'

        It ignores attributes that start with underscore and
        keys that already exist until ``overwrite`` is ``True``.

        :param object_: arbitrary object to update from,
                        or import path of that if it's a string
                        e.g. ``'myapp.configs:prod``
        :param overwrite: keys that already exist are ignored by default.
                          if ``True`` has given to this parameter,
                          these are not overwritten
        :type overwrite: :class:`bool`

        """
        if isinstance(object_, basestring):
            object_ = import_string(object_)
        for key in dir(object_):
            if not key.startswith('_') and (overwrite or key not in self):
                self[key] = getattr(object_, key)

    def update_from_file(self, filename, overwrite=False):
        """Updates configuration from Python file.
        For example, if there's :file:`dev.cfg`::

            debug = False
            database_uri = 'sqlite://'

        so you can load it using :meth:`update_from_file()` method::

            config.update_from_file('dev.cfg')

        Like :meth:`update_from_object()` method, it also ignores
        variables that start with underscore.

        :param filename: the path of Python file to load
        :type filename: :class:`basestring`
        :param overwrite: keys that already exist are ignored by default.
                          if ``True`` has given to this parameter,
                          these are not overwritten
        :type overwrite: :class:`bool`

        """
        module = ModuleType(filename)
        module.__file__ = abspath(filename)
        execfile(filename, module.__dict__)
        self.update_from_object(module, overwrite)

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

