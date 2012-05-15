""":mod:`plastic.version` --- Version data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

#: (:class:`tuple`) The triple of version numbers e.g. ``(1, 2, 3)``.
VERSION_INFO = (0, 1, 0)

#: (:class:`str`) The version string e.g. ``'1.2.3'``.
VERSION = '{0}.{1}.{2}'.format(*VERSION_INFO)


if __name__ == '__main__':
    print VERSION

