from __future__ import absolute_import, unicode_literals
import sys
from functools import reduce
if sys.version_info.major >= 3:
    from builtins import map
    from builtins import filter
else:
    from itertools import imap as map
    from itertools import ifilter as filter
