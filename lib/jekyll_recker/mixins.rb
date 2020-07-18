# frozen_string_literal: true

require 'logger'

module JekyllRecker
  module Mixins
    # Logging
    module Logging
      def self.included(base)
        base.extend(self)
      end

      def logger
        @logger ||= Logger.new(
          STDOUT,
          formatter: proc { |_severity, _datetime, _progname, msg| "jekyll-recker: #{msg}\n" }
        )
      end
    end
  end
end
