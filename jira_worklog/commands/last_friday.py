from __future__ import absolute_import, unicode_literals, print_function

from .base import get_last_weekday_date, print_worklog_events_by_date


FRIDAY_WEEKDAY = 4


def command():
    date = get_last_weekday_date(FRIDAY_WEEKDAY)
    print_worklog_events_by_date(date)
