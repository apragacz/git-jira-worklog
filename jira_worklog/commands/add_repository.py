from __future__ import absolute_import, unicode_literals, print_function
import os

from ..exceptions import CommandError
from ..config import get_default_team_config, retrieve_config, save_config


def prepare_parser(parser):
    parser.add_argument('team')
    parser.add_argument('repo_dir')


def command(team, repo_dir):
    if not os.path.exists(repo_dir):
        raise CommandError('please provide existing repository directory')

    repo_dir = os.path.abspath(repo_dir)

    config = retrieve_config()
    team_cfg = config['teams'].setdefault(team, get_default_team_config())
    repo_dirs = team_cfg['repository_directories']
    if repo_dir not in repo_dirs:
        repo_dirs.append(repo_dir)

    team_cfg['repository_directories'] = sorted(repo_dirs)
    save_config(config)
