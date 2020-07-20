# frozen_string_literal: true

module JekyllRecker
  module Generators
    # Word Count Generator
    class Words < Jekyll::Generator
      include BaseGenerator
      include Stats
      include Graphs

      KEY = 'words'

      def crunch
        total_counts = entries.collect(&:content).map { |c| number_of_words(c) }
        if production?
          logger.info 'production detected. skipping graphs'
          return
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

      def make_graph(posts)
        g = new_line_graph
        g.labels = Hash[posts.reverse.each_with_index.map { |p, i| [i, p.date.strftime("%a")] }]
        g.data :words, posts.collect(&:content).map { |c| number_of_words(c) }.reverse
        g.title = 'This Week'
        g.x_axis_label = 'Day'
        g.y_axis_label = 'Word Count'
        g.minimum_value = 0
        g.write(graphs_join('words.png'))
      end
    end
  end
end
