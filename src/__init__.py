# flake8: noqa

"""
This is the source code from my blog.  To execute the build, just run
the package like this:

```
./venv/bin/python -m src
```
"""

# functions
from .args import load_args
from .docs import write_api_docs
from .logging import load_logger
from .models.feed import load_feed
from .models.image import load_images
from .models.page import load_entries, load_pages
from .models.site import load_site
from .template import render_template
from .testing import run_unit_tests
from .utils import pave_webroot
from .validate import validate_html_references

# Models
from .models import (
    Site,
    Page,
    Image,
    Feed,
)


__all__ = [
    load_args,
    load_entries,
    load_feed,
    load_images,
    load_logger,
    load_pages,
    load_site,
    pave_webroot,
    run_unit_tests,
    validate_html_references,
    write_api_docs,
    Site,
    Page,
    Image,
    Feed,
]
