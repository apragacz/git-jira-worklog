from __future__ import absolute_import, unicode_literals, print_function
import os
import os.path
import json


def get_base_dirpath():
    home_dir = os.environ['HOME']
    return os.path.join(home_dir, '.config', 'git-jira-worklog')


def get_config_filepath():
    return os.path.join(get_base_dirpath(), 'config.json')


def get_default_config():
    return {
        'teams': {},
    }


def get_default_team_config():
    return {
        'repository_directories': [],
    }


def retrieve_config():
    config_path = get_config_filepath()
    config_data = get_default_config()
    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config_data.update(json.load(f))
    return config_data


def save_config(config_data):
    config_path = get_config_filepath()
    dirname = os.path.dirname(config_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(config_path, 'wt') as f:
        json.dump(config_data, f, indent=2, sort_keys=True)


def add_repository_directory(config_data, team, repo_dir):
    team_cfg = config_data['teams'].setdefault(team, get_default_team_config())
    repo_dirs = team_cfg['repository_directories']
    if repo_dir not in repo_dirs:
        repo_dirs.append(repo_dir)

    team_cfg['repository_directories'] = sorted(repo_dirs)


def get_repository_directories(config_data, team):
    team_cfg = config_data['teams'].get(team, get_default_team_config())
    return team_cfg['repository_directories']


def get_teams(config_data):
    return config_data['teams'].keys()
