import logging.config


def new_logging_config(level):
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': 'blog: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': level,
                'propagate': True
            }
        }
    }


def configure_logging(verbose=False):
    level = 'DEBUG' if verbose else 'INFO'
    config = new_logging_config(level)
    logging.config.dictConfig(config)
