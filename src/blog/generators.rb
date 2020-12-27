# frozen_string_literal: true

require 'jekyll'
require 'rake'

module Blog
  # Generators
  module Generators
    # Base
    module Base
      include Blog::Logging
      include Blog::Time
    end

    # Stats Generator
    class Stats < Jekyll::Generator
      include Base
      include Blog::Math

      attr_reader :site

      def generate(site)
        @site = Site.new(site)
        site.data['stats'] = if @site.production?
                               info 'calculating statistics'
                               real_stats
                             else
                               info 'stubbing out statistics'
                               stub_stats
                             end
      end

      def real_stats
        {
          'total_words' => total(site.word_counts),
          'average_words' => average(site.word_counts).round(0),
          'total_posts' => site.entries.size,
          'consecutive_posts' => consecutive_posts,
          'swears' => calculate_swears
        }
      end

      def stub_stats
        {
          'total_words' => 0,
          'average_words' => 0,
          'total_posts' => 0,
          'consecutive_posts' => 0,
          'swears' => 0
        }
      end

      private

      def consecutive_posts
        calculate_streaks(site.dates).first['days']
      end

      def calculate_swears
        results = Hash[count_swears]
        results['total'] = total(results.values)
        results
      end

      def count_swears
        occurences(swears, site.words).reject { |_k, v| v.zero? }.sort_by { |_k, v| -v }
      end

      def swears
        %w[
          ass asshole booger
          crap damn fart fuck hell jackass
          piss poop shit
        ]
      end
    end

    # GitGenerator
    class GitGenerator < Jekyll::Generator
      include Base
      include Blog::Git

      attr_reader :site

      def generate(site)
        @site = Site.new(site)
        site.data.merge!(data)
      end

      def data
        if site.production?
          info 'reading git history'
          real_data
        else
          info 'stubbing out git history'
          stub_data
        end
      end

      def real_data
        {
          'git_head' => git_head,
          'git_head_summary' => git_head_summary,
          'git_shorthead' => git_short_head,
          'git_commit_count' => git_commit_count
        }
      end

      def stub_data
        {
          'git_head' => '',
          'git_head_summary' => '',
          'git_shorthead' => '',
          'git_commit_count' => 0
        }
      end
    end

    # ResizeGenerator
    class ResizeGenerator < Jekyll::Generator
      include Base

      def generate(site); end
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
              'permalink' => "/#{to_filename_date(post.date)}.html",
              'filename' => "#{to_filename_date(post.date)}.html"
            }
          )
        end
      end
    end

    # Nav Generator
    class NavGenerator < Jekyll::Generator
      include Base

      attr_reader :site

      def generate(site)
        @site = Site.new(site)
        info 'building site navigation'
        site.data['nav'] = nav
      end

      def nav
        flagged_pages.sort_by { |p| p.data['nav'].to_i }
      end

      def flagged_pages
        site.pages.select { |p| p.data.key? 'nav' }
      end
    end

    # CoverageGenerator
    class CoverageGenerator < Jekyll::Generator
      include Base
      include Blog::Files
      include Blog::Shell

      def generate(site)
        info 'reading code coverage'
        data_file = join('_site/coverage/data.json')
        site.data['coverage'] = JSON.parse(File.read(data_file))
      end
    end
  end
end
