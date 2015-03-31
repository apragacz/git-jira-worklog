from __future__ import absolute_import, unicode_literals
from functools import reduce


def compose(*args):
    '''composes the list of function into one'''
    return reduce(lambda g, f: (lambda elem: f(g(elem))), reversed(args))


def identity(elem):
    '''identity function'''
    return elem


def ilimit(iterable, limit=100, offset=0):
    '''filter the iterable'''
    end_offset = offset + limit
    for i, elem in enumerate(iterable):
        if offset <= i and i < end_offset:
            yield elem
        elif end_offset <= i:
            return


def group_by(elements, key):

    def add_to_group(elem_groups, elem):
        last_group = elem_groups[-1] if len(elem_groups) > 0 else ()
        if not last_group:
            return elem_groups[:-1] + [(elem,)]
        elif key(last_group[0]) == key(elem):
            return elem_groups[:-1] + [last_group + (elem,)]
        else:
            return elem_groups + [(elem,)]

    return reduce(add_to_group, elements, [])
