from __future__ import absolute_import, unicode_literals, print_function
import argparse
import importlib
import pkgutil
import sys

from . import commands
from .exceptions import CommandError


cmd_map = {}


def add_command(subparsers, cmd_module):
    cmd_name = cmd_module.__name__.rsplit('.')[-1].replace('_', '-')
    cmd_map[cmd_name] = cmd_module.command

    cmd_parser = subparsers.add_parser(cmd_name)
    if hasattr(cmd_module, 'prepare_parser'):
        cmd_module.prepare_parser(cmd_parser)


def add_commands(subparsers):
    for _, modname, ispkg in pkgutil.iter_modules(commands.__path__):
        if ispkg:
            continue
        if modname == 'base':
            continue
        cmd_module_name = 'jira_worklog.commands.{}'.format(modname)
        cmd_module = importlib.import_module(cmd_module_name)
        add_command(subparsers, cmd_module)


def default_command(*args):
    print('invalid command', file=sys.stderr)


def main(args):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='sub_command')
    add_commands(subparsers)
    namespace = parser.parse_args(args[1:])
    cmd = cmd_map[namespace.sub_command]
    cmd_kwargs = vars(namespace)
    cmd_kwargs.pop('sub_command')
    try:
        cmd(**cmd_kwargs)
    except CommandError as exc:
        print('git-jira-worklog: error: {}'.format(exc.message), file=sys.stderr)
        sys.exit(1)


def entry_point():
    return main(sys.argv)
