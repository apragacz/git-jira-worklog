from __future__ import absolute_import, unicode_literals, print_function

from .base import get_last_weekday_date, print_worklog_events_by_date


WEEKDAYS = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday'
]

WEEKDAYS_INDICES_MAP = {wd: i for i, wd in enumerate(WEEKDAYS)}


def prepare_parser(parser):
    parser.add_argument('weekday', choices=WEEKDAYS)


def command(weekday):
    weekday_index = WEEKDAYS_INDICES_MAP[weekday]
    date = get_last_weekday_date(weekday_index)
    print_worklog_events_by_date(date)
