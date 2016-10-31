from __future__ import unicode_literals, print_function

from jira_worklog.exceptions import GitError
from jira_worklog.git import get_issue, get_current_branch


def command():
    branch = get_current_branch()
    try:
        issue_id = get_issue()
        print('Issue is set to \'{}\' for branch \'{}\''.format(
            issue_id, branch))
    except GitError:
        print('Issue is not set for branch \'{}\''.format(branch))
