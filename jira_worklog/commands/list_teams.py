from __future__ import absolute_import, unicode_literals, print_function

from ..config import get_teams, retrieve_config


def command():
    config_data = retrieve_config()
    for team in get_teams(config_data):
        print(team)
