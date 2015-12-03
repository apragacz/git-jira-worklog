from __future__ import absolute_import, unicode_literals, print_function
import itertools
import sys
from functools import reduce


class bcolors:
    HEADER = b'\033[95m'
    OKBLUE = b'\033[94m'
    OKGREEN = b'\033[92m'
    WARNING = b'\033[93m'
    FAIL = b'\033[91m'
    ENDC = b'\033[0m'
    BOLD = b'\033[1m'
    UNDERLINE = b'\033[4m'


def cprint(*objects, **kwargs):
    sep = kwargs.pop('sep', ' ')
    end = kwargs.pop('end', '\n')
    file = kwargs.pop('file', sys.stdout)
    color = kwargs.pop('color', None)

    if kwargs:
        raise TypeError(
            'cprint() got an unexpected keyword argument \'{}\''.format(
                next(iter(kwargs))
            ))

    if color is None:
        print(*objects, sep=sep, end=end, file=file)
    else:
        print(color, end='', file=file)
        print(*objects, sep=sep, end=end, file=file)
        print(bcolors.ENDC, end='', file=file)


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
    for group_key, group_iter in itertools.groupby(elements, key=key):
        yield list(group_iter)


def next_pair(iterator):
    try:
        elem = next(iterator)
        return (elem, True)
    except StopIteration:
        return (None, False)
