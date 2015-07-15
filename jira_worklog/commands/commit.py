from __future__ import unicode_literals, print_function
import os
import tempfile

from ..exceptions import GitError
from ..git import get_issue


def prepare_parser(parser):
    parser.add_argument('args', nargs='*')


def command(args):
    try:
        issue_id = get_issue()
        issue_prefix = '{} '.format(issue_id)
    except GitError:
        issue_prefix = ''

    with tempfile.NamedTemporaryFile() as f:
        f.write(issue_prefix)
        f.flush()
        cmd_args = ['git', 'commit']
        cmd_args.extend(args)
        cmd_args.append('--template')
        cmd_args.append(f.name)
        os.system(' '.join(cmd_args))
