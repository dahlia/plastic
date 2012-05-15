""":mod:`plastic.app` --- Application factories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import sys
import dis


class BaseApp(object):
    """The application base class."""

    @classmethod
    def clone(cls, __module__=None, __name__=None, **values):
        """Subclasses the application class.  It is a just shorthand of
        normal subclassing.  If your application becomes bigger stop
        using this and normaly subclass the application class
        using :keyword:`class` keyword instead.

        """
        try:
            getframe = sys._getframe
        except AttributeError:
            pass
        else:
            frame = getframe(1)
            if __module__ is None:
                __module__ = frame.f_globals.get('__name__')
            if __name__ is None:
                code = frame.f_code.co_code[frame.f_lasti:]
                code = code[3 if ord(code[0]) >= dis.HAVE_ARGUMENT else 1:]
                stores = (dis.opmap['STORE_NAME'],
                          dis.opmap['STORE_GLOBAL'],
                          dis.opmap['STORE_FAST'])
                opcode = ord(code[0])
                if opcode in stores:
                    name_pos = ord(code[1])
                    if opcode == dis.opmap['STORE_FAST']:
                        index = frame.f_code.co_varnames
                    else:
                        index = frame.f_code.co_names
                    try:
                        __name__ = index[name_pos]
                    except IndexError:
                        pass
        if __name__ is None:
            __name__ = 'App'
        subclass = type(__name__, (cls,), values)
        subclass.__module__ = __module__
        return subclass

