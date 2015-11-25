from __future__ import unicode_literals
import os.path
import subprocess

from .exceptions import GitError


def get_git_dir(repo_path):
    return os.path.join(repo_path, '.git')


def get_git_command_data(command_name, repo_path=None):
    cmd = ['git']
    if repo_path:
        cmd.append('--git-dir={}'.format(repo_path))
    cmd.append(command_name)
    return cmd


def get_git_rootdir(repo_path=None):
    cmd = get_git_command_data('rev-parse', repo_path=repo_path)
    cmd.append('--show-toplevel')
    dirpath = subprocess.check_output(cmd).rstrip()
    if not os.path.exists(dirpath):
        raise GitError('git directory {} does not exists'.format(dirpath))
    return dirpath


def get_git_config(config_name, repo_path=None):
    cmd = get_git_command_data('config', repo_path=repo_path)
    cmd.append(config_name)
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


def get_email(repo_path=None):
    return get_git_config('user.email', repo_path=repo_path)


def get_project_name(repo_path=None):
    return get_git_config('jiraworklog.projectname', repo_path=repo_path)


def set_project_name(project):
    set_git_config('jiraworklog.projectname', project)


def get_current_branch(repo_path=None):
    cmd = get_git_command_data('branch', repo_path=repo_path)
    try:
        data = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        raise GitError('git branch failed')
    for line in data.decode('utf-8').split('\n'):
        if line.startswith('*'):
            return line[1:].strip()
    raise GitError('current branch not found')


def get_issue(repo_path=None):
    branch = get_current_branch(repo_path=repo_path)
    return get_git_config('branch.{}.issue'.format(branch),
                          repo_path=repo_path)


def set_issue(issue):
    branch = get_current_branch()
    # TODO: test pattern
    set_git_config('branch.{}.issue'.format(branch), issue)


def get_git_log_file(include_all=True, repo_path=None):
    cmd = get_git_command_data('log', repo_path=repo_path)
    cmd.append('--format=%H %at %ae %s')
    if include_all:
        cmd.append('--all')
    pipe = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        close_fds=True,
    )
    return pipe.stdout
