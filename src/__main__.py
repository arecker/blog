from . import pages as _  # noqa:F401
from . import lib


def main():
    args = lib.parse_args()
    lib.configure_logging(verbose=args.verbose)

    if args.hook:
        lib.run_pre_commit_hook()
        return

    if args.fixup:
        lib.fixup_project(entries_dir=args.dir_entries)
        return

    info = lib.load_info(args.dir_data)
    entries = lib.fetch_entries(args.dir_entries)

    if args.tweet:
        lib.share_latest_as_tweet(latest=entries[0],
                                  full_url=info.url,
                                  creds_dir=args.dir_secrets,
                                  dry=args.dry)
        return

    pages = lib.fetch_pages()

    lib.write_sitemap(args.dir_www,
                      full_url=info.url,
                      entries=entries,
                      pages=[p.filename for p in pages])

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


if __name__ == '__main__':
    main()
