import blog
import logging

logger = logging.getLogger(__name__)

# @blog.register_page(filename='index.html',
#                     title='Dear Journal',
#                     description='Daily, public journal by Alex Recker')
# def index(page, entries=[]):
#     try:
#         latest = entries[0]
#         page.block('h2', 'Latest Post')
#         with page.wrapping_block('a', href=f'./{latest.filename}'):
#             page.block('h3', latest.title)
#             page.figure(
#                 src=f'./images/banners/{latest.banner}',
#                 href=f'./{latest.filename}',
#                 caption=latest.description,
#                 alt='banner image for latest post',
#             )
#     except IndexError:
#         logger.warn('no entries found, skipping latest post')

#     return page


@blog.register_command
def build(args):
    """Build the website locally"""

    entries = blog.all_entries(args.dir_entries)
    logger.info('retrieved %d entries from %s', len(entries), args.dir_entries)

    blog.write_sitemap(args.dir_www, full_url=args.site_url, entries=entries)

    blog.write_entries(entries,
                       dir_www=str(args.dir_www),
                       full_url=str(args.site_url),
                       author=args.site_author,
                       year=args.site_year)


def main():
    blog.main()


if __name__ == '__main__':
    main()
