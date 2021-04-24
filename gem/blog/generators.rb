# frozen_string_literal: true

require 'jekyll'

module Blog
  # Generators
  module Generators
    # Base
    module Base
      include Blog::Logging
      include Blog::Time
    end

    # FrontmatterGenerator
    class FrontmatterGenerator < Jekyll::Generator
      include Base

      def generate(site)
        info 'setting default frontmatter'
        scan_pages!(site)
        scan_posts!(site)
      end

      def scan_pages!(site)
        site.pages.each do |page|
          filename = "#{File.basename(page.name, '.*')}.html"
          page.data['filename'] = filename
          page.data['permalink'] = filename if page.data['permalink'].nil?
        end
      end

      def scan_posts!(site)
        site.posts.docs.each do |post|
          post.data.merge!(
            {
              'title' => to_uyd_date(post.date),
              'description' => post.data['title'],
              'excerpt' => post.data['title'],
              'image' => "/images/banners/#{post.data['banner']}",
              'permalink' => "/#{to_filename_date(post.date)}.html",
              'filename' => "#{to_filename_date(post.date)}.html"
            }
          )
        end
      end
    end
  end
end
