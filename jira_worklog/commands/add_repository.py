from __future__ import absolute_import, unicode_literals, print_function
import os

from ..exceptions import CommandError
from ..config import add_repository_directory, retrieve_config, save_config


def prepare_parser(parser):
    parser.add_argument('team')
    parser.add_argument('repo_dir')


def command(team, repo_dir):
    if not os.path.exists(repo_dir):
        raise CommandError('please provide existing repository directory')

    repo_dir = os.path.abspath(repo_dir)

    config_data = retrieve_config()
    add_repository_directory(config_data, team, repo_dir)
    save_config(config_data)
