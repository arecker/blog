# frozen_string_literal: true

module JekyllRecker
  # Generators Module
  module Generators
    # Stats Generator
    class Stats < Jekyll::Generator
      include Date
      include Logging
      include Math

      attr_reader :site

      def generate(site)
        @site = Site.new(site)
        info 'calculating statistics'
        site.data['stats'] = stats
      end

      def stats
        @stats ||= {
          'total_words' => total(site.word_counts),
          'average_words' => average(site.word_counts),
          'total_posts' => site.entries.size,
          'consecutive_posts' => calculate_streaks(site.dates).first['days'],
          'swears' => calculate_swears
        }
      end

      private

      def calculate_swears
        results = Hash[count_swears]
        results['total'] = total(results.values)
        results
      end

      def count_swears
        occurences(swears, site.words).reject { |_k, v| v.zero? }.sort_by { |_k, v| -v }
      end

      def swears
        site.recker_config.fetch('swears', [])
      end
    end

    # Graphs Generator
    class Graphs < Jekyll::Generator
      include Logging

      attr_reader :site

      def generate(site)
        @site = Site.new(site)
        if @site.production? && @site.recker_config.fetch('production_skip_graphs', true)
          info 'skipping graphs (production)'
        else
          info 'generating graphs'
          JekyllRecker::Graphs.generate_graphs(@site)
        end
      end
    end

    # Image Resize Generator
    class ImageResize < Jekyll::Generator
      require 'fastimage'
      require 'mini_magick'

      include Logging

      attr_reader :site

      def generate(site)
        @site = Site.new(site)
        if @site.production? && @site.recker_config.fetch('production_skip_images', true)
          info 'skipping image resizing (production)'
        else
          info 'checking images sizes'
          resizeable_images.each do |f, d|
            info "resizing #{f} to fit #{d}"
            image = MiniMagick::Image.new(f)
            image.resize d
          end
        end
      end

      def too_big?(width, height)
        width > 800 || height > 800
      end

      def images_without_graphs
        site.images.reject { |i| i.include?('/graphs/') }
      end

      def resizeable_images
        with_sizes = images_without_graphs.map { |f| [f, FastImage.size(f)].flatten }
        with_sizes.select! { |f| too_big?(f[1], f[2]) }
        with_sizes.map do |f, w, h|
          dimensions = if w > h
                         '800x600'
                       else
                         '600x800'
                       end
          [f, dimensions]
        end
      end
    end

    # Code Coverage Generator
    class CodeCoverage < Jekyll::Generator
      include Logging

      attr_reader :site

      def generate(site)
        @site = Site.new(site)
        info 'running tests'
        Shell.run 'rspec'
        info 'reading code coverage'
        @site.data['coverage'] = JSON.parse(File.read(tmp_file))
      end

      private

      def tmp_file
        site.tmp_join('coverage.json')
      end
    end

    # Yard Generator
    class Yard < Jekyll::Generator
      include Logging

      attr_reader :site

      def generate(site)
        @site = Site.new(site)
        info 'generating documentation'
        Shell.run "yard -o #{@site.site_join('doc')} -q"
      end
    end

    # Git History Generator
    class GitHistory < Jekyll::Generator
      include Logging

      attr_reader :site

      def generate(site)
        @site = Site.new(site)
        info 'reading git history'
        site.data['git'] = {
          'commit_count' => commit_count
        }
      end

      def commit_count
        @commit_count ||= Shell.run('git rev-list --count master').chomp
      end
    end
  end
end

