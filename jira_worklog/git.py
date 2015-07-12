from __future__ import unicode_literals
import os.path
import subprocess

from .exceptions import GitError


def get_git_rootdir():
    cmd = ['git', 'rev-parse', '--show-toplevel']
    dirpath = subprocess.check_output(cmd).rstrip()
    if not os.path.exists(dirpath):
        raise GitError('git directory {} does not exists'.format(dirpath))
    return dirpath


def get_git_config(config_name):
    cmd = ['git', 'config', config_name]
    try:
        data = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        raise GitError(
            'Value for {name} is not specified. '
            'Please specify it using the command:\n'
            'git config {name} <value>'.format(
                name=config_name,
            )
        )
    return data.decode('utf-8').rstrip()


def set_git_config(config_name, value):
    cmd = ['git', 'config', config_name, value]
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        raise GitError('git config failed')


def get_email():
    return get_git_config('user.email')


def get_project_name():
    return get_git_config('jiraworklog.projectname')


def set_project_name(project):
    set_git_config('jiraworklog.projectname', project)


def get_current_branch():
    cmd = ['git', 'branch']
    try:
        data = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        raise GitError('git branch failed')
    for line in data.decode('utf-8').split('\n'):
        if line.startswith('*'):
            return line[1:].strip()
    raise GitError('current branch not found')


def get_issue():
    branch = get_current_branch()
    return get_git_config('branch.{}.issue'.format(branch))


def set_issue(issue):
    branch = get_current_branch()
    # TODO: test pattern
    set_git_config('branch.{}.issue'.format(branch), issue)


def get_git_log_file():
    pipe = subprocess.Popen(
        ['git', 'log', '--format=%H %at %ae %s'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        close_fds=True,
    )
    return pipe.stdout
