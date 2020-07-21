# frozen_string_literal: true

module JekyllRecker
  module Generators
    # Streak Count Generator
    class Streaks < Jekyll::Generator
      include Stats

      KEY = 'days'

      def crunch
        calculate_streaks(dates).first
      end
    end
  end
end
