from __future__ import unicode_literals
import os.path
import subprocess

from .exceptions import CommandError


def get_git_rootdir():
    cmd = ['git', 'rev-parse', '--show-toplevel']
    dirpath = subprocess.check_output(cmd).rstrip()
    if not os.path.exists(dirpath):
        raise ValueError('git directory {} does not exists'.format(dirpath))
    return dirpath


def get_git_config(config_name):
    cmd = ['git', 'config', config_name]
    try:
        data = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        raise CommandError(
            'Value for {name} is not specified. '
            'Please specify it using the command:\n'
            'git config {name} <value>'.format(
                name=config_name,
            )
        )
    return data.decode('utf-8').rstrip()


def get_email():
    return get_git_config('user.email')


def get_project_name():
    return get_git_config('jiraworklog.projectname')


def get_git_log_file():
    pipe = subprocess.Popen(
        ['git', 'log', '--format=%H %at %ae %s'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        close_fds=True,
    )
    return pipe.stdout
