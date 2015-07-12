from __future__ import unicode_literals, print_function

from ..exceptions import GitError
from ..git import get_project_name, set_project_name


def prepare_parser(parser):
    parser.add_argument('name', nargs='?')


def command(name):
    if name is None:
        try:
            name = get_project_name()
            print('Project name is \'{}\''.format(name))
        except GitError:
            print('Project name is not set')
    else:
        set_project_name(name)
        print('Project name set to \'{}\''.format(name))
