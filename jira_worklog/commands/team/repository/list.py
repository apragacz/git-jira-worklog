from __future__ import absolute_import, unicode_literals, print_function

from jira_worklog.config import get_repository_directories, retrieve_config


def prepare_parser(parser):
    parser.add_argument('team')


def command(team):
    config_data = retrieve_config()
    for repo_path in get_repository_directories(config_data, team):
        print(repo_path)
