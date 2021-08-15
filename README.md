# blog

This is the source code for my blog, [alexrecker.com]

[alexrecker.com]: https://www.alexrecker.com

## Installing

Don't be a fancy pants.  Just use a hecking alias.

```shell
alias b='cd ~/src/blog && python -m src
```

## Usage

To see all the available subcommands, just run the command.

    alex@console:~/src/blog$ b
    usage: blog [-h] [-s] [-v] [-d] [-r ROOT_DIRECTORY] {build,images,jenkins,pave,publish,serve,help} ...

    blog - the greatest static HTML journal generator ever made

    positional arguments:
      {build,images,jenkins,pave,publish,serve,help}
        build               build the website locally
        images              resize all images in the webroot
        jenkins             run full CI pipeline
        pave                delete all generated files in webroot
        publish             publish working files as a new entry
        serve               serve webroot locally
        help                print program usage

    optional arguments:
      -h, --help            show this help message and exit
      -s, --silent          hide all logs
      -v, --verbose         print debug logs
      -d, --debug           step through code interactively
      -r ROOT_DIRECTORY, --root_directory ROOT_DIRECTORY
                            path to blog root directory

## Markup

Make pages and entries with regular HTML.

### Metadata

Use special comments to give each page metadata.

Example:

```html
<!-- meta:title Some Page -->
<!-- meta:description This is some page on my website. -->
```

### Navigation

Control which pages show up in the site navigation with the special
`nav` metadata comment.

```html
<!-- meta:nav 2 -->

<p>This page will be the second link in the navigation bar!</p>
```

### Magic Comments

Display dynamic information on your web page with magic comments.

Before:

```html
<!-- blog:latest -->
```

After:

```html
<!-- begin blog:latest -->
<a href="/2021-08-13.html">
  <h3 class="title">Friday, August 13 2021</h3>
</a>
<figure>
  <a href="/2021-08-13.html">
    <img src="/images/banners/2021-08-13.jpg">
  </a>
  <figcaption>
    <p>chicago, sleep walking, and the beetle cannibalism tax</p>
  </figcaption>
</figure>
<!--end blog:latest-->
```

| Comment        | Description                                    |
|----------------|------------------------------------------------|
| `blog:latest`  | Renders latest journal entry.                  |
| `blog:entries` | Renders a complete list of entries in a table. |
