""":mod:`plastic.resourcedir` --- Resources directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections

from pkg_resources import (resource_exists, resource_isdir, resource_listdir,
                           resource_stream)


class ResourceDirectory(collections.Mapping):
    """Mapping interface of package resources."""

    def __init__(self, package, directory=''):
        self.package = package
        if directory and not directory.endswith('/'):
            directory += '/'
        self.directory = directory

    def __iter__(self):
        def iterate(path):
            for name in resource_listdir(self.package, self.directory + path):
                yield name
                if resource_isdir(self.package,
                                  self.directory + path + '/' + name):
                    for subname in iterate(path + '/' + name):
                        yield name + '/' + subname
        return iterate('')

    def __contains__(self, name):
        subname = self.directory + name
        return (resource_exists(self.package, subname) or
                resource_isdir(self.package, subname))

    def __getitem__(self, name):
        subname = self.directory + name
        if resource_isdir(self.package, subname):
            return type(self)(self.package, subname)
        elif resource_exists(self.package, subname):
            file_ = resource_stream(self.package, subname)
            return Resource(file_)
        raise KeyError(name)

    def __len__(self):
        i = 0
        for _ in self:
            i += 1
        return i


class Resource(object):
    """Readable file object provided by :class:`ResourceDirectory` mapping
    objects.  You can treat this simply as file object.  It also is a
    context manager, so you can use it using :keyword:`with`.

    :param file_: file to wrap

    """

    def __init__(self, file_):
        self.file_ = file_

    def read(self, *args, **kwargs):
        return self.file_.read(*args, **kwargs)

    def close(self):
        self.file_.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

