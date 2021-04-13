# frozen_string_literal: true

require 'date'
require 'time'

module Blog
  # Time
  module Time
    def time_to_date(time)
      ::Date.parse(time.strftime('%Y-%m-%d'))
    end

    def date_to_time(date)
      date.to_time.to_datetime
    end

    def to_uyd_date(date)
      date.strftime('%A, %B %-d %Y')
    end

    def to_filename_date(date)
      date.strftime('%Y-%m-%d')
    end

    def parse_date(datestr)
      ::Date.parse(datestr).to_datetime.new_offset(offset).to_date
    end

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
