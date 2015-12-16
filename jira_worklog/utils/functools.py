from __future__ import absolute_import, unicode_literals
from .compat import reduce


def build_pipe(*args):
    '''builds a pipe (a processing function) of the list of functions'''
    return reduce(lambda g, f: (lambda elem: f(g(elem))), args)


def compose(*args):
    '''composes the list of function into one'''
    return build_pipe(reversed(args))


def identity(elem):
    '''identity function'''
    return elem
