from __future__ import absolute_import, unicode_literals, print_function
import datetime

from .day import print_worklog_events_by_date


def command():
    date = datetime.date.today() - datetime.timedelta(days=1)
    print_worklog_events_by_date(date)
