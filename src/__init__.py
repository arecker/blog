# flake8: noqa

"""
This is the source code for my blog.  This library is comprised of
functions and objects for working with all website resources.

To add a new script, simply create a new file python file in
`src/scripts/`.  Invoke the script by running `python -m
src.scripts.<name>`.

You can import the `src` library into your code like this.

```python
import src

src.pave_webroot()  # off you go!
```
"""

# functions
from .args import load_args
from .context import make_global_context
from .feed import build_feed_items
from .logging import load_logger
from .models.image import load_images
from .models.page import load_entries, load_pages
from .models.site import load_site
from .template import render_template
from .utils import pave_webroot

from .models import (
    Site,
    Page,
    Image,
)


__all__ = [
    load_args,
    load_entries,
    load_images,
    load_logger,
    load_pages,
    load_site,
    pave_webroot,
    Site,
    Page,
    Image,
]
