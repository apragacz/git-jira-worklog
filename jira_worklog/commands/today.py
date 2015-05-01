from __future__ import absolute_import, unicode_literals, print_function
import datetime

from .day import print_worklog_events_by_date


def command(*args):
    date = datetime.date.today()
    print_worklog_events_by_date(date)
