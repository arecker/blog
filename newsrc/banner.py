class BannerMixin(object):
    '''
    Page Mixin, for working with banners.
    '''
    @property
    def banner_context(self):
        if self.banner_filename:
            return {
                'banner_full_url': self.banner_full_url,
                'banner_relative_url': self.banner_relative_url,
            }
        else:
            return {}

    @property
    def banner_filename(self):
        return self.metadata.get('banner')

    @property
    def banner_relative_url(self):
        if self.banner_filename:
            return f'/images/banners/{self.banner_filename}'

    @property
    def banner_full_url(self):
        if self.banner_filename:
            base = 'https://www.alexrecker.com'
            return f'{base}/images/banners/{self.banner_filename}'
