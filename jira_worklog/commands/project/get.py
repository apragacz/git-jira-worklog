from __future__ import unicode_literals, print_function

from jira_worklog.exceptions import GitError
from jira_worklog.git import get_project_name


def command(name):
    try:
        name = get_project_name()
        print('Project name is \'{}\''.format(name))
    except GitError:
        print('Project name is not set')
