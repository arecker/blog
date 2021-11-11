"""functions for expanding magic comment macros"""

import logging

logger = logging.getLogger(__name__)


def expand_text(html, site=None, suppress_logs=False):
    simple_macros = []

    timestamp_format = '%A, %B %d %Y %-I:%M %p'
    if zone := site.timestamp.tzname():
        timestamp_format += f' {zone}'
    else:
        timestamp_format += ' CST'
        if not suppress_logs:
            logger.warn('no timezone set, defaulting to CST')

    simple_macros.append(
        ('<!-- blog:timestamp -->', site.timestamp.strftime(timestamp_format)))

    for macro, expansion in simple_macros:
        html = html.replace(macro, expansion)

    return html
