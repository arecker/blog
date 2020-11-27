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

    # TimeGenerator
    class TimeGenerator < Jekyll::Generator
      include Base

      def generate(site)
        info 'generating build time'
        site.data.merge!(
          {
            'year' => today.year,
            'last_updated' => to_timestamp(now)
          }
        )
      end
    end

    # GitGenerator
    class GitGenerator < Jekyll::Generator
      include Base
      include Blog::Git

      def generate(site)
        info 'reading git history'
        site.data.merge!(
          {
            'git_head' => git_head,
            'git_head_summary' => git_head_summary,
            'git_shorthead' => git_short_head
          }
        )
      end
    end

    # ResizeGenerator
    class ResizeGenerator < Jekyll::Generator
      include Base

      def generate(site)

      end
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
          filename = File.basename(page.name, '.*') + '.html'
          page.data['filename'] = filename
          if page.data['permalink'].nil?
            debug "setting permalink to #{filename}"
            page.data['permalink'] = filename
          else
            debug "skipping #{page.name}, set to #{page.data['permalink']}"
          end

        end
      end

      def scan_posts!(site)
        site.posts.docs.each do |post|
          post.data.merge!(
            {
              'title' => to_uyd_date(post.date),
              'description' => post.data['title'],
              'permalink' => "/#{to_filename_date(post.date)}.html",
              'filename' => "#{to_filename_date(post.date)}.html"
            }
          )
        end
      end
    end
  end
end
