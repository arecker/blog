# frozen_string_literal: true

module JekyllRecker
  module Generators
    # Swear Count Generator
    class Swears < Jekyll::Generator
      include Stats

      KEY = 'swears'

      def crunch
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
