Blog
====

![](https://travis-ci.org/arecker/Blog.svg?branch=master)

This is my blog.

It's the actual blog, posts and all, so it would really be of no use to you to clone this repo.
However, if you'd like to mimic the design, you are free to.

## Building it locally

The easiest way to get a local build going is with ```python virtualenv```, which is probably available for your platform.  Once you have the ```virtualenv``` command in your bin, build a local environment and install the dependencies.

```bash
$ cd Blog
$ virtualenv .env && ./.env/bin/pip install -r requirements.txt
```

Next, you can create a simple ```blog``` script as a wrapper for the virtual environment and ```blog.py```

```bash
#!/bin/bash
/path/to/Blog/.env/bin/python /path/to/Blog/blog.py "$@"
```

If all went well, you should have a callable ```blog``` script.

```bash
$ blog
Usage: blog.py [OPTIONS] COMMAND [ARGS]...

  This is the script for my blog.  It does things.

Options:
  --help  Show this message and exit.

Commands:
  email   manages the email subscription engine
  server  run the web server
  test    run unit tests
  update  refresh the content cache
```

Update the cache folder and run the local web server
```bash
blog update && blog server
```

That's all!  More inline documentation in the app.
