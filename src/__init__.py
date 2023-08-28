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

from .context import make_global_context
from .feed import build_feed_items
from .logging import configure_logging
from .media import load_images, Image
from .models import Page
from .template import render_template
from .utils import pave_webroot

__all__ = [
    build_feed_items,
    configure_logging,
    load_images,
    make_global_context,
    pave_webroot,
    render_template,
    Page,
    Image,
]
