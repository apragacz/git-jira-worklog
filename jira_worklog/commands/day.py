from __future__ import absolute_import, unicode_literals, print_function
import datetime
from functools import partial

from ..events import event_from_gitlog, group_events, pretty_form_tuple
from ..exceptions import CommandError
from ..git import get_email, get_git_log_file, get_project_name
from ..utils import compose, ilimit


def get_worklog_events(date=None):
    email = get_email()
    project_name = get_project_name()
    if not email:
        raise CommandError('No email set')
    if not project_name:
        raise CommandError('No project name set')

    p_out = get_git_log_file()
    process = compose(
        group_events,
        partial(sorted, key=lambda e: e.datetime),
        partial(filter, lambda e: e.datetime.date() == date),
        partial(filter, lambda e: e.author_email == email),
        partial(ilimit, limit=1000),
        partial(map, partial(event_from_gitlog, project_name=project_name))
    )
    result = process(p_out)
    p_out.close()
    return result


def print_worklog_events_by_date(date):
    for event_group in get_worklog_events(date):
        print(pretty_form_tuple(event_group))


def command(date_string=None, *args):
    try:
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise CommandError('Date not in form YYYY-MM-DD')

    print_worklog_events_by_date(date)
