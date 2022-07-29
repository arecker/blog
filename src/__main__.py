from . import pages as _  # noqa:F401
from . import lib


def main():
    args = lib.parse_args()
    lib.configure_logging(verbose=args.verbose)

    if args.hook:
        lib.run_pre_commit_hook()
        return

    info = lib.load_info(args.dir_data)
    entries = lib.fetch_entries(args.dir_entries)
    pages = lib.fetch_pages()

    lib.pave_webroot(www_dir=args.dir_www)

    lib.write_sitemap(args.dir_www,
                      full_url=info.url,
                      entries=entries,
                      pages=[p.filename for p in pages])

    lib.write_redirects(www_dir=args.dir_www, data_dir=args.dir_data)

    lib.write_feed(args.dir_www,
                   title=info.title,
                   subtitle=info.title,
                   author_name=info.author,
                   author_email=info.email,
                   timestamp=entries[0].date,
                   full_url=info.url,
                   entries=entries[:50])

    lib.write_entries(entries=entries,
                      dir_www=str(args.dir_www),
                      full_url=info.url,
                      author=info.author)

    lib.write_pages(
        dir_www=str(args.dir_www),
        entries=entries,
        pages=pages,
        full_url=info.url,
        author=info.author,
        args=args,
    )

    lib.validate_website(args.dir_www)


if __name__ == '__main__':
    main()
