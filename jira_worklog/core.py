from __future__ import absolute_import, unicode_literals, print_function
import sys

from .commands import day
from .exceptions import CommandError


def main(args):
    try:
        cmd = args[1] if len(args) > 1 else None
        if cmd == 'day':
            day.command(*args[2:])
        else:
            print('invalid command', file=sys.stderr)
    except CommandError as exc:
        print(exc.args[0], file=sys.stderr)


def entry_point():
    return main(sys.argv)
