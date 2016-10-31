from __future__ import unicode_literals, print_function

from jira_worklog.git import set_project_name


def prepare_parser(parser):
    parser.add_argument('name')


def command(name):
    set_project_name(name)
    print('Project name set to \'{}\''.format(name))
