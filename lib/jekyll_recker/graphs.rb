# frozen_string_literal: true

require 'bundler'

module JekyllRecker
  # Graphs module
  module Graphs
    def generate_graphs(posts, swears, graphs_dir)
      WordCount.new(posts, graphs_dir).write
      Swears.new(swears, graphs_dir).write
    end

    # Word Count Graph
    class WordCount
      def initialize(posts, graphs_dir)
        @posts = posts[0..6].reverse
        @graphs_dir = graphs_dir
      end

      def graphs_join(path)
        File.join Bundler.root, @graphs_dir, path
      end

      def title
        format = '%m/%d/%y'
        first = @posts.first.date.strftime(format)
        last = @posts.last.date.strftime(format)
        "Word Count: #{first} - #{last}"
      end

      def labels
        Hash[@posts.each_with_index.map { |p, i| [i, p.date.strftime('%a')] }]
      end

      # TODO: copied from jekyll
      def number_of_words(input)
        input.split.length
      end

      def write
        g = Gruff::Line.new('800x600')
        g.theme = Gruff::Themes::PASTEL
        g.hide_legend = true
        g.labels = labels
        g.data :words, @posts.collect(&:content).map { |c| number_of_words(c) }
        g.title = title
        g.x_axis_label = 'Day'
        g.y_axis_label = 'Word Count'
        g.minimum_value = 0
        g.write(graphs_join('words.png'))
      end
    end

    # Swears Chart
    class Swears
      attr_reader :results

      def initialize(results, graphs_dir)
        @results = results
        @graphs_dir = graphs_dir
      end

      # TODO: I SUCK
      def graphs_join(path)
        File.join Bundler.root, @graphs_dir, path
      end

      def write
        g = Gruff::Pie.new('800x600')
        g.theme = Gruff::Themes::PASTEL
        g.hide_legend = false
        g.legend_at_bottom = true
        g.minimum_value = 0
        results.each { |w, n| g.data w, n }
        g.write(graphs_join('swears.png'))
      end
    end
  end
end
