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

from .template import render_template, render_page, write_page, prettify_xml
from .page import load_pages, load_entries
from .context import make_global_context
from .media import load_images, Image
from .feed import build_feed_items
from .utils import pave_webroot

__all__ = [
    build_feed_items,
    load_entries,
    load_images,
    load_pages,
    make_global_context,
    pave_webroot,
    prettify_xml,
    render_page,
    render_template,
    write_page,
    Image,
]
