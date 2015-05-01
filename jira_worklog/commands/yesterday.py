from __future__ import absolute_import, unicode_literals, print_function
import datetime

from ..events import pretty_form_tuple
from .day import get_worklog_events


def command(*args):
    date = datetime.date.today() - datetime.timedelta(days=1)

    for event in get_worklog_events(date):
        print(pretty_form_tuple(event))
