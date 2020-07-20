# frozen_string_literal: true

module JekyllRecker
  module Generators
    # Streak Count Generator
    class Streaks < Jekyll::Generator
      include Stats

      KEY = 'days'

      def crunch
        streaks.take(1).map do |count, dates|
          {
            'days' => count,
            'start' => dates[0],
            'end' => dates[1]
          }
        end.first
      end

      private

      def streaks
        _streaks = []
        entry_dates.slice_when do |prev, curr|
          curr != prev - 1
        end.each do |dates|
          first, last = dates.minmax
          _streaks << [(last - first).to_i, [first, last]]
        end
        _streaks
      end

      def entry_dates
        entries.collect(&:date).map { |t| Date.new(t.year, t.month, t.day) }.sort.reverse
      end
    end
  end
end
