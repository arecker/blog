# blog

This is the source code for my blog, [alexrecker.com]

[alexrecker.com]: https://www.alexrecker.com

## Installing

Don't be a fancy pants.  Just use a hecking alias.

```shell
alias b='cd ~/src/blog && python -m blog
```

## Usage

To see all the available subcommands, just run the `b` command.

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
