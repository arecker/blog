# frozen_string_literal: true

require 'bundler'

module JekyllRecker
  # Graphs module
  module Graphs
    def self.generate_graphs(site)
      require 'gruff'
      WordCount.new(site).write
      Swears.new(site).write
    end

    # Base Graph
    module Base
      attr_reader :site

      def graphs_join(path)
        File.join Bundler.root, @graphs_dir, path
      end
    end

    # Word Count Graph
    class WordCount
      include Base

      def initialize(site)
        @site = site
        @graphs_dir = site.graphs_dir
      end

      def posts
        site.entries[0..6].reverse
      end

      def word_counts
        site.word_counts[0..6].reverse
      end

      def title
        format = '%m/%d/%y'
        first = posts.first.date.strftime(format)
        last = posts.last.date.strftime(format)
        "Word Count: #{first} - #{last}"
      end

      def labels
        Hash[posts.each_with_index.map { |p, i| [i, p.date.strftime('%a')] }]
      end

      def write
        g = ::Gruff::Line.new('800x600')
        g.theme = Gruff::Themes::PASTEL
        g.hide_legend = true
        g.labels = labels
        g.data :words, word_counts
        g.title = title
        g.x_axis_label = 'Day'
        g.y_axis_label = 'Word Count'
        g.minimum_value = 0
        g.write(graphs_join('words.png'))
      end
    end

    # Swears Chart
    class Swears
      include Base

      def initialize(site)
        @site = site
      end

      def results
        data = site.data['stats']['swears'].clone
        data.delete('total')
        data
      end

      def write
        g = ::Gruff::Pie.new('800x600')
        g.theme = Gruff::Themes::PASTEL
        g.hide_legend = false
        g.legend_at_bottom = true
        g.minimum_value = 0
        results.each { |w, n| g.data w, n }
        g.write(site.graphs_join('swears.png'))
      end
    end
  end
end
