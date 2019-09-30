# frozen_string_literal: true

require 'jekyll'

module Blog
  module Jekyll
    def self.build(config)
      conf = ::Jekyll.configuration(
        {
          'source' => config.blog_repo,
          'destination' => config.site_dir
        }
      )
      ::Jekyll::Site.new(conf).process
    end
  end
end
