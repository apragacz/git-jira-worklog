from __future__ import unicode_literals, print_function

from jira_worklog.exceptions import GitError
from jira_worklog.git import set_issue, get_current_branch


def prepare_parser(parser):
    parser.add_argument('issue_id')


def command(issue_id):
    branch = get_current_branch()
    set_issue(issue_id)
    print('Issue set to \'{}\' for branch \'{}\''.format(issue_id, branch))
