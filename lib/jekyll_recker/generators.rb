# frozen_string_literal: true

require 'bundler'

module JekyllRecker
  # Generators Module
  module Generators
    # Base Generator Functions
    module Base
      include Date
      include Logging
      include Math

      def production?
        ENV['JEKYLL_ENV'] == 'production'
      end

      def word_counts
        @word_counts ||= bodies.map(&:split).map(&:size)
      end

      def words
        bodies.map(&:split).flatten
      end

      def bodies
        entries.collect(&:content)
      end

      def entries
        @site.posts.docs.select(&:published?).sort_by(&:date).reverse
      end

      def dates
        entries.collect(&:date).map { |t| ::Date.new(t.year, t.month, t.day) }
      end
    end

    # Stats Generator
    class Stats < Jekyll::Generator
      include Base
      include Graphs

      def generate(site)
        @site = site
        logger.info 'calculating statistics'
        @site.data['stats'] = data
        if production?
          logger.info 'production detected. skipping graphs'
        else
          require 'gruff'
          logger.info 'generating graphs'
          generate_graphs(entries, swear_results, graphs_dir)
        end
      end

      def data
        {
          'total_words' => total(word_counts),
          'average_words' => average(word_counts),
          'total_posts' => entries.size,
          'consecutive_posts' => calculate_streaks(dates).first['days'],
          'swears' => {
            'total' => swear_results.map(&:last).reduce(0, :+),
            'words' => swear_results
          }
        }
      end

      private

      def swear_results
        @swear_results ||= count_swears
      end

      def graphs_dir
        recker = @site.config.fetch('recker', {})
        recker.fetch('graphs', 'assets/images/graphs/')
      end

      def count_swears
        results = Hash.new(0)
        bodies.map(&:split).each do |words|
          words = words.map(&:downcase)
          swears.each do |swear|
            count = words.count(swear)
            results[swear] += count
          end
        end
        results.reject { |_k, v| v.zero? }.sort_by { |_k, v| -v }
      end

      def swears
        %w[
          ass
          asshole
          booger
          crap
          damn
          fart
          fuck
          hell
          jackass
          piss
          poop
          shit
        ]
      end
    end
    require 'jekyll_recker/generators/image_resize.rb'
  end
end
