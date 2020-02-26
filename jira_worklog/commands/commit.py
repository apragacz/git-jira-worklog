from __future__ import unicode_literals, print_function
import os
import tempfile

from ..exceptions import GitError
from ..git import get_issue


BOOL_OPTIONS = (
    ('--all', '-a'),
    ('--patch', '-p'),
    ('--reset-author',),
    ('--short',),
    ('--branch',),
    ('--porcelain',),
    ('--long',),
    ('--null', '-z'),
    ('--signoff', '-s'),
    ('--no-verify', '-n'),
    ('--allow-empty',),
    ('--allow-empty-message',),
    ('--edit', '-e'),
    ('--no-edit',),
    ('--amend',),
    ('--no-post-rewrite',),
    ('--include', '-i'),
    ('--only', '-o'),
    ('--verbose', '-v'),
    ('--quiet', '-q'),
    ('--dry-run',),
    ('--status',),
    ('--no-status',),
)

# without --template
VALUE_OPTIONS = (
    ('--reuse-message', '-C', 'commit'),
    ('--reedit-message', '-c', 'commit'),
    ('--fixup', None, 'commit'),
    ('--squash', None, 'commit'),
    ('--file', '-F'),
    ('--author',),
    ('--date',),
    ('--message', '-m', 'msg'),
    ('--cleanup', None, 'mode'),
    ('--untracked-files', '-u'),
    ('--gpg-sign', '-S', 'keyid'),
)


def create_map(option_list):
    option_map = {}
    for option_tuple in option_list:
        option = option_tuple[0]
        key = option.lstrip('-').replace('-', '_')
        option_map[key] = option
    return option_map


def prepare_parser(parser):
    for t in BOOL_OPTIONS:
        args = [t[0]]
        if len(t) > 1:
            args.append(t[1])
        kwargs = dict(action='store_true')
        parser.add_argument(*args, **kwargs)
    for t in VALUE_OPTIONS:
        args = [t[0]]
        if len(t) > 1 and t[1] is not None:
            args.append(t[1])
        if len(t) > 2:
            kwargs = dict(metavar=t[2])
        else:
            kwargs = {}
        parser.add_argument(*args, **kwargs)
    parser.add_argument('files', nargs='*', metavar='file')


def command(**kwargs):
    files = kwargs.pop('files')
    try:
        issue_id = get_issue()
        issue_prefix = '{} '.format(issue_id)
    except GitError:
        issue_prefix = ''

    bool_option_map = create_map(BOOL_OPTIONS)
    value_option_map = create_map(VALUE_OPTIONS)

    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.write(issue_prefix)
        f.flush()
        cmd_args = ['git', 'commit']
        for key, value in kwargs.items():
            if key in bool_option_map and value is True:
                cmd_args.append(bool_option_map[key])
            elif key in value_option_map and value is not None:
                cmd_args.append(value_option_map[key])
                cmd_args.append(value)

        cmd_args.extend(files)
        cmd_args.append('--template')
        cmd_args.append(f.name)
        os.system(' '.join(cmd_args))
