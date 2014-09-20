Blog
====

This is my blog.  It's a bunch of markdown files, jinja templates, and one python script that does everything.

### Building it Locally

To build this blog locally, install all the dependencies listed in ```requirements.txt``` on the machine or within a virtual environemnt.

```bash
$ pip install -r requirements.txt
```

Next, create a bash-python wrapper for the blog script and place it somewhere in your path.  It should look like this:

```bash
#!/bin/bash
/path/to/python /path/to/repo/Blog/blog.py "$@"
```

If all went well, ```blog``` should be a callable command.  It can be used to launch the local debuggin webserver, refresh the content cache, and even send emails.  There is more inline documentation in the script itself.
