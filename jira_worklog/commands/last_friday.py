from __future__ import absolute_import, unicode_literals, print_function
import datetime

from .day import print_worklog_events_by_date


FRIDAY_WEEKDAY = 4


def command(*args):
    date_today = datetime.date.today()
    if date_today.weekday() > FRIDAY_WEEKDAY:
        delta_days = date_today.weekday() - FRIDAY_WEEKDAY
    else:
        delta_days = date_today.weekday() + 7 - FRIDAY_WEEKDAY
    date = date_today - datetime.timedelta(delta_days)
    print_worklog_events_by_date(date)
