from __future__ import unicode_literals, print_function

from ..exceptions import GitError
from ..git import get_issue, set_issue, get_current_branch


def prepare_parser(parser):
    parser.add_argument('issue_id', nargs='?')


def command(issue_id):
    branch = get_current_branch()
    if issue_id is None:
        try:
            issue_id = get_issue()
            print('Issue is set to \'{}\' for branch \'{}\''.format(
                issue_id, branch))
        except GitError:
            print('Issue is not set for branch \'{}\''.format(branch))
    else:
        set_issue(issue_id)
        print('Issue set to \'{}\' for branch \'{}\''.format(
            issue_id, branch))
