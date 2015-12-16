from __future__ import absolute_import, unicode_literals
from .compat import reduce


def compose(*args):
    '''composes the list of function into one'''
    return reduce(lambda g, f: (lambda elem: f(g(elem))), reversed(args))


def identity(elem):
    '''identity function'''
    return elem
