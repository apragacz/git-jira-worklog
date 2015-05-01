from __future__ import absolute_import, unicode_literals, print_function
import sys

from .commands import day, today, yesterday
from .exceptions import CommandError


def main(args):
    try:
        cmd = args[1] if len(args) > 1 else None
        cmd_args = args[2:]
        if cmd == 'day':
            day.command(*cmd_args)
        elif cmd == 'today':
            today.command(*cmd_args)
        elif cmd == 'yesterday':
            yesterday.command(*cmd_args)
        else:
            print('invalid command', file=sys.stderr)
    except CommandError as exc:
        print(exc.args[0], file=sys.stderr)


def entry_point():
    return main(sys.argv)
