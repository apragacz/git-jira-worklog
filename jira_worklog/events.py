from __future__ import absolute_import, unicode_literals
import collections
import datetime
import re

from .utils import group_by


Event = collections.namedtuple('Event', (
    'commit_hash',
    'author_email',
    'datetime',
    'ticket',
    'comment'
))


def parse_full_comment(full_comment, project_name):
    comment_sp = full_comment.split(' ', 1)
    ticket_pat = '^({})\\-[0-9]+$'.format(project_name)
    ticket_re = re.compile(ticket_pat)
    if ticket_re.search(comment_sp[0]):
        ticket = comment_sp[0]
        if len(comment_sp) == 2:
            comment = comment_sp[1]
        else:
            comment = None
    else:
        ticket = None
        comment = full_comment
    return (ticket, comment)


def event_from_gitlog(line, project_name):
    splits = line.decode('utf8').strip().split(' ', 3)
    commit_hash = splits[0]
    timestamp = int(splits[1])
    author_email = splits[2]
    full_comment = splits[3]
    (ticket, comment) = parse_full_comment(full_comment, project_name)
    date_time = datetime.datetime.fromtimestamp(timestamp)
    return Event(
        commit_hash=commit_hash,
        datetime=date_time,
        ticket=ticket, comment=comment,
        author_email=author_email
    )


def group_events(events):
    return group_by(events, key=lambda e: e. ticket)


def pretty_form(event):
    return '{}'.format(event.comment)


def pretty_form_tuple(event_group):
    ticket = event_group[0].ticket if event_group[0].ticket else '<Unknown>'
    datetime_start = event_group[0].datetime
    datetime_end = event_group[-1].datetime
    return '\n{} {}-{}\n\n{}\n'.format(
        ticket, datetime_start.time(), datetime_end.time(),
        '\n'.join(pretty_form(event) for event in event_group)
    )
