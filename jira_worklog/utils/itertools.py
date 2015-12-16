from __future__ import absolute_import, unicode_literals, print_function
import itertools

from .compat import reduce


__all__ = ['limit', 'group_by', 'merge_sorted']


def limit(iterable, limit=100, offset=0):
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


class ForwardSequence(object):

    def __init__(self, iterable):
        self.last_index = -1
        self.last_value = None
        self.iter = iter(iterable)

    def __getitem__(self, key):
        delta = key - self.last_index

        if delta < 0:
            raise ValueError('cannot access this index')

        while delta:
            try:
                self.last_value = next(self.iter)
                self.last_index += 1
                delta -= 1
            except StopIteration:
                raise IndexError('index out of range')

        return self.last_value


def is_in_sequence(index, sequence):
    try:
        sequence[index]
        return True
    except IndexError:
        return False


def merge_two_sorted_sequences(seq1, seq2):
    i = j = 0
    while is_in_sequence(i, seq1) and is_in_sequence(j, seq2):
        a = seq1[i]
        b = seq2[j]
        if a < b:
            yield a
            i += 1
        else:
            yield b
            j += 1
    while is_in_sequence(i, seq1):
        yield seq1[i]
        i += 1
    while is_in_sequence(j, seq2):
        yield seq2[j]
        j += 1


def merge_sorted(iterable, *iterables):
    return reduce(lambda iterator, iterable: merge_two_sorted_sequences(
        ForwardSequence(iterator), ForwardSequence(iterable),
    ), iterables, iter(iterable))
