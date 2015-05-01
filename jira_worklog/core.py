from __future__ import absolute_import, unicode_literals, print_function
import sys

from .commands import day, last_friday, today, yesterday
from .exceptions import CommandError


cmd_map = {}


def add_command(cmd_module):
    cmd_name = cmd_module.__name__.rsplit('.')[-1].replace('_', '-')
    cmd_map[cmd_name] = cmd_module.command


def default_command(*args):
    print('invalid command', file=sys.stderr)


def main(args):
    add_command(day)
    add_command(today)
    add_command(yesterday)
    add_command(last_friday)

    cmd_name = args[1] if len(args) > 1 else None
    cmd = cmd_map.get(cmd_name, default_command)
    cmd_args = args[2:]
    try:
        cmd(*cmd_args)
    except CommandError as exc:
        print(exc.args[0], file=sys.stderr)


def entry_point():
    return main(sys.argv)
