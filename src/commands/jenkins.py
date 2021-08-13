'''
run full CI pipeline
'''

# environment {
#     NETLIFY_SITE_ID = credentials('netlify-blog-site-id')
#     NETLIFY_TOKEN = credentials('netlify-token')
#     PYENV_ROOT = '/var/lib/jenkins/.pyenv/'
# }

# Install
# ${PYENV_ROOT}/bin/pyenv install --skip-existing

# Test
# ${PYENV_ROOT}/shims/python -m unittest

# Build
# ${PYENV_ROOT}/shims/python -m src build

# Publish
# netlifyctl deploy -y -A "${NETLIFY_TOKEN}" -s "${NETLIFY_SITE_ID}" -m "jenkins: ${BUILD_TAG}"

import logging

logger = logging.getLogger(__name__)


def main(config=None, context=None):
    pass
