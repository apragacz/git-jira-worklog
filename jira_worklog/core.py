from __future__ import absolute_import, unicode_literals, print_function
import argparse
import importlib
import pkgutil
import sys

from . import commands
from .exceptions import WorklogError


def command_name_of_module_name(module_name):
    return module_name.rsplit('.')[-1].replace('_', '-')


def add_command(subparsers, cmd_module):
    cmd_name = command_name_of_module_name(cmd_module.__name__)
    cmd_parser = subparsers.add_parser(cmd_name)
    cmd_parser.set_defaults(func=cmd_module.command)
    if hasattr(cmd_module, 'prepare_parser'):
        cmd_module.prepare_parser(cmd_parser)


def add_subcommands(parser, cmd_module):
    subparsers = parser.add_subparsers()
    for _, modname, ispkg in pkgutil.iter_modules(cmd_module.__path__):
        if modname == 'base':
            continue
        sub_cmd_module_name = cmd_module.__name__ + '.' + modname
        sub_cmd_module = importlib.import_module(sub_cmd_module_name)
        if ispkg:
            sub_cmd_name = command_name_of_module_name(sub_cmd_module_name)
            sub_cmd_parser = subparsers.add_parser(sub_cmd_name)
            add_subcommands(sub_cmd_parser, sub_cmd_module)
        else:
            add_command(subparsers, sub_cmd_module)


def main(args):
    parser = argparse.ArgumentParser()
    add_subcommands(parser, commands)
    namespace = parser.parse_args(args[1:])
    cmd = namespace.func
    cmd_kwargs = vars(namespace)
    cmd_kwargs.pop('func')
    try:
        cmd(**cmd_kwargs)
    except WorklogError as exc:
        print('git-jira-worklog: error: {}'.format(exc.message), file=sys.stderr)
        sys.exit(1)


def entry_point():
    return main(sys.argv)
