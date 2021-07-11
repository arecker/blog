import sys

from newsrc.logger import logger


def parse_markdown(content):
    try:
        import markdown
        return markdown.markdown(content)
    except ImportError:
        logger.error(
            'markdown is not supported!  Please install the markdown pip package.'
        )
        sys.exit(1)
