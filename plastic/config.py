""":mod:`plastic.config` --- Configuration mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from keyword import iskeyword
from re import VERBOSE, compile
from os.path import abspath
from tokenize import Name
from types import ModuleType

from werkzeug.utils import import_string

__all__ = 'Config', 'get_typename', 'import_instance'


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


expression_pattern = compile(
    r'^(?P<import_string>' + Name + r'(?:\.' + Name + r')*(?::' + Name + r')?)'
    r'\s*(?:\((?P<arguments>.*?)\)\s*)?$'
)

expression_arguments_pattern = compile(r'''
    (?: ^ | ,) \s*
    (?:(?P<keyword> \w+) \s* = \s*)?
    (?P<argument>
        (?P<argument_none> None) |
        (?P<argument_bool> True | False) |
        (?P<argument_float> \d+\.(?:\d+)?) |
        (?P<argument_int> \d+) |
        (?P<argument_bareword> \w+) |
        (?P<argument_string>
            (?: [uU][rR] | [uU]|[rR])?
            (?: ' (?: [^'\\] | \\. )* ' | " (?: [^"\\] | \\. )* ")
        )
    )
    \s*
''', VERBOSE)


def import_instance(expression, type_):
    """This function provides a minimal language to import a class from
    a package/module and make an instance of it.  For example, the following
    code::

        val = import_instance('abc.defg:ClassName(3.14, hello, world=False)')

    is equivalent to the following normal Python code::

        from abc.defg import ClassName

        val = ClassName(3.14, 'hello', world=False)

    As you can see its syntax is slightly different from normal Python.
    You can pass arguments to class' constructor using its own syntax.
    You can pass limited types of values:

    Booleans
       You can pass ``True`` and ``False``.

    Numbers
       It can take integers and floating numbers e.g. ``123``, ``3.14``.

    Strings
       You can ``'single quote'`` and ``"double quote"`` both for string
       literals, and ``r'raw string literals'`` are also available.
       There are ``u'Unicode string literals'`` as well.

       Moreover, if there re unquoted barewords these are also interpreted
       as strings.

    None
       You can pass ``None``.

    """
    if not isinstance(type_, type):
        raise TypeError('type_ must be a class object, not ' + repr(type_))
    if issubclass(type_, basestring):
        raise TypeError('type_ cannot be basestring nor its subtype because '
                        'these are ambiguious to determine whether the given '
                        'value is an import expression or already an '
                        'instance of type_')
    if isinstance(expression, basestring):
        match = expression_pattern.match(expression)
        if not match:
            raise ValueError('invalid import expression: ' + repr(expression))
        import_name = match.group('import_string')
        cls = import_string(import_name)
        if not isinstance(cls, type):
            raise TypeError(
                '{0} ({1!r}) is not a class object'.format(import_name, cls)
            )
        if not issubclass(cls, type_):
            raise TypeError(
                '{0} ({1!r}) is not a subtype of {2} ({3!r})'.format(
                    import_name, cls, get_typename(type_), type_
                )
            )
        arguments = match.group('arguments')
        if arguments:
            arguments_offset = match.start('arguments')
            offset = 0
            args = []
            kwargs = {}
            for match in expression_arguments_pattern.finditer(arguments):
                keyword = match.group('keyword')
                print (keyword, match.start(), offset, arguments)
                if match.start() > offset or not keyword and kwargs:
                    raise ValueError(
                        'invalid expression:\n' + expression + '\n' +
                        ' ' * (offset + arguments_offset) + '^'
                    )
                argument = match.group('argument_bareword')
                if not argument:
                    argument = eval(match.group('argument'))
                if keyword:
                    kwargs[keyword] = argument
                else:
                    args.append(argument)
                offset = match.end()
            if offset < len(arguments):
                raise ValueError('invalid expression:\n' + expression + '\n' +
                                 ' ' * (offset + arguments_offset) + '^')
            instance = cls(*args, **kwargs)
        else:
            instance = cls()
        if not isinstance(instance, type_):
            raise TypeError(
                '{0} is not an instance of {1}'.format(expression,
                                                       get_typename(type_))
            )
    else:
        instance = expression
        if not isinstance(instance, type_):
            raise TypeError(
                '{0!r} is not an instance of {1}'.format(instance,
                                                         get_typename(type_))
            )
    return instance


def get_typename(cls):
    """Finds the typename string of the given ``cls``.

    :param cls: the class object to find its typename
    :type cls: :class:`type`
    :returns: the typename
    :rtype: :class:`basestring`

    """
    mod = cls.__module__
    if mod in ('__main__', '__builtin__'):
        return cls.__name__
    return mod + '.' + cls.__name__

