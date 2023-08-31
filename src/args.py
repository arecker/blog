import argparse


parser = argparse.ArgumentParser(
    'src.scripts.build',
    description='Build the website to the local file system',
)
group = parser.add_argument_group('Run options')
group.add_argument(
    '--verbose',
    default=False,
    action='store_true',
    help='print debug logs'
)

group = parser.add_argument_group('Directories')
group.add_argument('--dir-www', default='./www')
group.add_argument('--dir-entries', default='./entries')
group.add_argument('--dir-pages', default='./pages')
group.add_argument('--dir-templates', default='./templates')
group.add_argument('--dir-images', default='./www/images')

group = parser.add_argument_group('Site Options')
group.add_argument('--site-title', required=True)
group.add_argument('--site-description', required=True)
group.add_argument('--site-protocol', default='https')
group.add_argument('--site-domain', required=True)
group.add_argument('--site-author', required=True)
group.add_argument('--site-email', required=True)


def load_args() -> argparse.Namespace:
    """
    Load the system args against the standard website parser.

    ```python
    args = src.load_args()
    logger.debug('called with args = %s', vars(args))
    ```
    """
    return parser.parse_args()
