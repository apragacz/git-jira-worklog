from __future__ import absolute_import, unicode_literals, print_function
import datetime
from functools import partial

from ..config import get_repository_directories, retrieve_config
from ..events import event_from_gitlog, group_events, pretty_form_tuple
from ..exceptions import CommandError
from ..git import get_email, get_git_log_file, get_project_name
from ..utils.printing import bcolors, cprint
from ..utils.compat import filter, map
from ..utils.functools import build_pipe
from ..utils.itertools import merge_sorted


def get_last_weekday_date(weekday):
    date_today = datetime.date.today()
    if date_today.weekday() > weekday:
        delta_days = date_today.weekday() - weekday
    else:
        delta_days = date_today.weekday() + 7 - weekday
    date = date_today - datetime.timedelta(delta_days)
    return date


def get_worklog_events(date, repo_path=None):
    email = get_email(repo_path=repo_path)
    project_name = get_project_name(repo_path=repo_path)
    if not email:
        raise CommandError('No email set')
    if not project_name:
        raise CommandError('No project name set')

    p_out = get_git_log_file(repo_path=repo_path)
    process_into_events = build_pipe(
        partial(map, partial(event_from_gitlog, project_name=project_name)),
        partial(filter, lambda e: e.author_email == email),
        partial(filter, lambda e: e.datetime.date() == date),
        partial(sorted, key=lambda e: e.datetime),
    )
    events = process_into_events(p_out)
    p_out.close()
    return events


def get_worklog_event_groups(date, team=None):
    if team is not None:
        config_data = retrieve_config()
        repo_paths = get_repository_directories(config_data, team)
        if not repo_paths:
            raise CommandError('No repositories for team {}'.format(team))
        events = merge_sorted(*[get_worklog_events(date, repo_path)
                                for repo_path in repo_paths])
    else:
        events = get_worklog_events(date)

    events_groups = group_events(events)
    return events_groups


def print_worklog_events_by_date(date, team=None):
    event_groups = get_worklog_event_groups(date, team=team)
    if not event_groups:
        cprint('JIRA worklog for {} is empty.'.format(date),
               color=bcolors.BOLD)
        return
    cprint('JIRA worklog for {}:'.format(date),
           color=bcolors.BOLD)

    for event_group in event_groups:
        print(pretty_form_tuple(event_group))
