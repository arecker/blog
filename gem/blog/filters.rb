# frozen_string_literal: true

require 'liquid'

module Blog
  # Filters
  module Filters
    def uyd_date(date)
      date.strftime('%A, %B %-d %Y')
    end

    def pretty(num)
      num.to_s.reverse.gsub(/(\d{3})(?=\d)/, '\\1,').reverse
    end
  end
end

::Liquid::Template.register_filter(Blog::Filters)
