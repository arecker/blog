# frozen_string_literal: true

module JekyllRecker
  # Math Module
  module Math
    def average(numlist)
      calc = numlist.inject { |sum, el| sum + el }.to_f / numlist.size
      calc.round
    end

    def total(numlist)
      numlist.inject(0) { |sum, x| sum + x }
    end

    def slice_by_consecutive_days(dates)
      dates.slice_when { |p, c| c != p - 1 && c != p + 1 }.to_a
    end

    def calculate_streaks(dates)
      slice_by_consecutive_days(dates).map do |pair|
        first, last = pair.minmax
        [(last - first).to_i, [first, last]]
      end
    end
  end
end
