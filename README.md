Blog
====

This is my blog.  It changes a lot, but this is what it happens to look like now.

### Building it Locally

To build this project locally, it is recomended to install [python virtualenv](https://pypi.python.org/pypi/virtualenv), which is likely available for your platform.

Once that is going, clone the project locally and load up a new environment with the project's required dependencies:

    $ git clone https://github.com/arecker/Blog.git
    $ cd Blog
    $ virtualenv .env
    $ ./.env/bin/pip install -r requirements.txt

Once the brief installation finishes, create a new ```blog``` script in your bin, which will serve as a simple wrapper for the environment.  After modifying the script below with your path, paste it into ```blog```:

    #!/bin/bash
    PATH="/path/to/Blog/" # <-- Add path here
    cd $PATH
    ./.env/bin/python ./src/cli.py "$@"
  
If all went well, the app is now callable with your script.

```
    $ blog
      Usage: cli.py [OPTIONS] COMMAND [ARGS]...
      
      This is the script for my blog. It does things.
    
      Options:
        --help  Show this message and exit.
    
      Commands:
        email    manage email subscribers
        preview  preview a post in html
        refresh  refresh the content of the public folder
```
    
This script can be used to refresh the content cache, manage email subscriptions (private .keys.json file required), and preview a markdown post in html.  There is plenty more inline documentation for using the script.

### Editing a post

This package uses markdown metadata for file information.  Each post should start like the one below:
```
    Title: This is My Post
    Description: This is a short description of my post.  It can be a bit longer.
    Image: http://picturesite.com/image
  
    This is the first line of my post.
```
The Image attribute is not required for a valid post, but if it is included, the URL must be fully qualified ("http://...").

### Previewing a post

To preview a post, call the ```blog``` script with the command ```preview``` and the path to your valid markdown file.

    $ blog preview /home/me/Desktop/post.md
    
This will generate an HTML file in the current directory and open it in your browser.

### Publishing a post

When the post is ready to be published, rename it according to the date (YYYY-MM-DD.md) and commit it to the ```posts``` directory.  The script should take care of the rest.

### TODO:
- Automate post publishing
- Clean up email command
