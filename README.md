# blog

This is the source code from [alexrecker.com]

[alexrecker.com]: https://www.alexrecker.com

## Installing

Don't be a fancy pants.  Just use a hecking alias.

```shell
alias b='cd ~/src/blog && python -m blog'
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
