# frozen_string_literal: true

module JekyllRecker
  # Generators Module
  module Generators
    # Base Generator
    module Base
      include Date
      include Logging
      include Math

      attr_reader :site

      def name
        self.class.name.split('::').last.downcase
      end

      def generate(site)
        @site = Site.new(site)
        if @site.production?
          info "skipping #{name} generator"
        else
          info "running #{name} generator"
          data = crunch
          File.open(data_file_target, 'w') { |f| f.write(JSON.pretty_generate(data)) } unless data.nil?
        end
      end

      def data_file_target
        File.join site.data_dir, "#{name}.json"
      end
    end

    # Stats Generator
    class Stats < Jekyll::Generator
      include Base

      attr_reader :site

      def crunch
        generate_stats
      end

      def generate_stats
        {
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
      include Base

      def crunch
        JekyllRecker::Graphs.generate_graphs(site)
        nil
      end
    end

    # Git Generator
    class Git < Jekyll::Generator
      include Base

      def crunch
        {
          'commit_count' => Shell.run('git rev-list --count master').chomp
        }
      end
    end

    # Image Resize Generator
    class ImageResize < Jekyll::Generator
      include Base

      def crunch
        load_deps!
        info 'checking images'
        resizeable_images.each do |f, d|
          info "resizing #{f} to fit #{d}"
          image = MiniMagick::Image.new(f)
          image.resize d
        end
        nil
      end

      def too_big?(width, height)
        width > 800 || height > 800
      end

      def load_deps!
        require 'fastimage'
        require 'mini_magick'
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
  end
end
