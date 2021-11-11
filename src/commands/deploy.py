"""deploy site to Netlify"""

import logging

from src import netlify
from src.models import Site
from src.commands import build

logger = logging.getLogger(__name__)


def register(subparser):
    subparser.add_argument('--netlify-token',
                           required=True,
                           help='Netlify API token')


def main(args):
    build.main(args)
    site = Site(args=args)
    logger.info('deploying site')
    netlify.deploy(site_name=site.domain,
                   token=args.netlify_token,
                   webroot=site.directory / 'www')
