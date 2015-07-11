from __future__ import absolute_import, unicode_literals, print_function
import datetime

from .base import print_worklog_events_by_date


def command():
    date = datetime.date.today()
    print_worklog_events_by_date(date)
