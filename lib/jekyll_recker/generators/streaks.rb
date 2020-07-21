# frozen_string_literal: true

module JekyllRecker
  module Generators
    # Streak Count Generator
    class Streaks < Jekyll::Generator
      include Stats

      KEY = 'days'

      def crunch
        calculate_streaks(entry_dates).first
      end

      def entry_dates
        entries.collect(&:date).map { |t| Date.new(t.year, t.month, t.day) }.sort.reverse
      end
    end
  end
end
