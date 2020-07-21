# frozen_string_literal: true

module JekyllRecker
  module Generators
    # Word Count Generator
    class Words < Jekyll::Generator
      include Base
      include Stats
      include Graphs

      KEY = 'words'

      def crunch
        total_counts = entries.collect(&:content).map { |c| number_of_words(c) }
        if production?
          logger.info 'production detected. skipping graphs'
        else
          require 'gruff'
          logger.info 'generating wordcount graphs'
          make_graph(entries[0..6])
        end
        {
          'average' => average(total_counts),
          'total' => total(total_counts)
        }
      end

      def labels(posts)
        Hash[posts.reverse.each_with_index.map { |p, i| [i, p.date.strftime("%a")] }]
      end

      def title(posts)
        format = '%m/%d/%y'
        first = posts.last.date.strftime(format)
        last = posts.first.date.strftime(format)
        "Word Count: #{first} - #{last}"
      end

      def make_graph(posts)
        g = new_line_graph
        g.labels = labels(posts)
        g.data :words, posts.collect(&:content).map { |c| number_of_words(c) }.reverse
        g.title = title(posts)
        g.x_axis_label = 'Day'
        g.y_axis_label = 'Word Count'
        g.minimum_value = 0
        g.write(graphs_join('words.png'))
      end
    end
  end
end
