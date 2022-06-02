"""share latest entry in a slack post"""

import collections
import json
import logging
import pathlib
import urllib.parse

from . import http

logger = logging.getLogger(__name__)

Workspace = collections.namedtuple('Workspace', ['name', 'webhook_url'])


def load_workspaces(secrets_dir):
    workspaces = []
    with (pathlib.Path(secrets_dir) / 'slack.json').open('r') as f:
        for k, v in json.load(f).items():
            workspace = Workspace(name=k, webhook_url=v)
            workspaces.append(workspace)
    logger.debug('loaded %d slack workspaces from secrets/slack.json')
    return workspaces


def share_latest_as_slack(latest=None, full_url='', secrets_dir='', dry=False):
    url = urllib.parse.urljoin(full_url, latest.filename)
    message = '\n'.join([latest.title, latest.description, url])
    payload = {
        'text': message,
        'channel': '#blog',
        'username': 'reckerbot',
        'icon_emoji': ':reckerbot:',
    }

    for workspace in load_workspaces(secrets_dir):
        if dry:
            logger.warn('running in dry, but would have posted %s to slack',
                        payload)
        else:
            http.make_http_request(url=workspace.webhook_url,
                                   method='POST',
                                   data=payload)
        logger.info('shared "%s" to slack workspace %s', latest.description,
                    workspace.name)
