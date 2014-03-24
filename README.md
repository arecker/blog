Blog
====

This is the source code (and basically the entirety) of my blog.

I don't know what I'm doing here.  I just got really tired of Wordpress plugins and decided to roll my own Amish CMS.

### server.py
This is the file that holds the routes, the controllers, and helper methods.

### fragments/
This is where the common HTML widgets are stored

### metas/
This is simply where the meta <head> info is kept for pages and posts

### posts/
This is where the post html is stored


## Putting it all together
Based on the request, the server will determine which page to retrieve.  After the page name is passed into a helper function, the function assembles the HTML fragments, concatenates them, and returns them to the controller.
