# frozen_string_literal: true

module JekyllRecker
  module Generators
    # Swear Count Generator
    class Swears < Jekyll::Generator
      include Stats
      include Graphs

      KEY = 'swears'

      def crunch
        results = calculate
        if production?
          logger.info 'production detected. skipping graphs'
        else
          logger.info 'generating bad word graph'
          make_graph(results)
        end
        {
          "words" => results,
          "total" => results.map(&:last).reduce(0, :+)
        }
      end

      def make_graph(results)
        require 'gruff'
        g = new_pie_graph
        g.legend_at_bottom = true
        g.minimum_value = 0
        results.each { |w, n| g.data w, n }
        g.write(graphs_join('swears.png'))
      end

      def calculate
        results = Hash.new(0)
        entries.collect(&:content).map(&:split).each do |words|
          words = words.map(&:downcase)
          swears.each do |swear|
            count = words.count(swear)
            results[swear] += count
          end
        end
        results.reject { |_k, v| v.zero? }.sort_by { |_k, v| -v }
      end

      private

      def swears
        [
          'ass',
          'asshole',
          'booger',
          'crap',
          'damn',
          'fart',
          'fuck',
          'hell',
          'jackass',
          'piss',
          'poop',
          'shit',
        ]
      end
    end
  end
end
