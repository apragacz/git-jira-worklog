from __future__ import absolute_import, unicode_literals, print_function
import datetime

from ..exceptions import CommandError
from .base import print_worklog_events_by_date


def prepare_parser(parser):
    parser.add_argument('date_string')


def command(date_string):
    try:
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise CommandError('Date not in form YYYY-MM-DD')

    print_worklog_events_by_date(date)
