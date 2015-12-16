from __future__ import absolute_import, unicode_literals, print_function
import datetime

from .base import print_worklog_events_by_date


def prepare_parser(parser):
    parser.add_argument('--team', '-t')


def command(team):
    date = datetime.date.today() - datetime.timedelta(days=1)
    print_worklog_events_by_date(date, team)
