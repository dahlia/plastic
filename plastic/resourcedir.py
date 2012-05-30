""":mod:`plastic.resourcedir` --- Resources directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections
import contextlib

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
            return contextlib.closing(file_)
        raise KeyError(name)

    def __len__(self):
        i = 0
        for _ in self:
            i += 1
        return i

