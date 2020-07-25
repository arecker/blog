# frozen_string_literal: true

module JekyllRecker
  # Date Module
  module Date
    def slice_by_consecutive(dates)
      dates.slice_when { |p, c| c != p - 1 && c != p + 1 }.to_a
    end

    def calculate_streaks(dates)
      slice_by_consecutive(dates).map do |pair|
        first, last = pair.minmax
        {
          'days' => (last - first).to_i,
          'start' => first,
          'end' => last
        }
      end
    end
  end
end
