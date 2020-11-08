import logging.config
import os


def configure_logging():
    if os.environ.get('DEBUG') == '1':
        level = 'DEBUG'
    else:
        level = 'INFO'

    default_logging_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(name)s: %(message)s'
            },
        },
        'handlers': {
            'standard': {
                'level': level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
            },
        },
        'loggers': {
            '': {
                'handlers': ['standard'],
                'level': level,
                'propagate': False
            },
            'blog': {
                'handlers': ['standard'],
                'level': level,
                'propagate': False
            },
        }
    }

    logging.config.dictConfig(default_logging_config)
